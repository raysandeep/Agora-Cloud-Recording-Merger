import subprocess
import shlex
import shutil
import boto3
import os
from django.conf import settings
from celery.task import task
from .models import ChannelStatus
from glob import glob
from botocore.client import Config


@task(name="process", serializer='json')
def bg_process(channel_id, options):
    channel = ChannelStatus.objects.filter(channel_id=channel_id)
    if not channel.exists():
        return False
    channel = channel[0]
    channel.status = 'Downloading Files from S3'
    channel.save()
    Utils.downloadDirectoryFroms3(channel_id)
    channel.status = 'Processing'
    channel.save()
    Utils.merge_files(channel_id, options)
    channel.status = 'Uploading the output to S3'
    channel.save()
    if options['merge_mode'] == 2:
        Utils.upload_to_s3(channel_id, "m4a")
        channel.aws_key = channel_id+".m4a"
    else:
        Utils.upload_to_s3(channel_id, "mp4")
        channel.aws_key = channel_id+".mp4"
    Utils.clean_up(channel_id)
    channel.status = 'Completed'
    channel.save()
    return True


class Utils:

    @staticmethod
    def downloadDirectoryFroms3(channel_id):
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        bucket = s3_resource.Bucket(settings.AWS_BUCKET_NAME)
        print(bucket.objects.filter(Prefix=channel_id))
        for obj in bucket.objects.filter(Prefix=channel_id):
            print(obj)
            if not os.path.exists(os.path.dirname(os.path.join(settings.MEDIA_ROOT, obj.key))):
                os.makedirs(os.path.dirname(
                    os.path.join(settings.MEDIA_ROOT, obj.key)))
            bucket.download_file(obj.key, os.path.join(
                settings.MEDIA_ROOT, obj.key))

        print("Downloading from S3")

    @staticmethod
    def upload_to_s3(channel_id, file_ext):
        filename = channel_id+"."+file_ext
        s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY,
                            aws_secret_access_key=settings.AWS_SECRET_KEY)
        s3.Bucket(
            settings.AWS_OUTPUT_BUCKET_NAME
        ).upload_file(
            os.path.join(settings.MEDIA_ROOT, "outputs/"+filename),
            filename
        )
        os.remove(os.path.join(settings.MEDIA_ROOT,
                               "outputs/"+filename))  # Clean Local

        return True

    @staticmethod
    def clean_up(channel_id):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, channel_id))
        for i in glob(os.path.join(settings.MEDIA_ROOT,  "outputs/"+channel_id)+"*"):
            os.remove(i)
        return True

    @staticmethod
    def get_mergable_list(channel_id):
        file = open(os.path.join(settings.MEDIA_ROOT,
                                 "outputs/{channel_id}.txt".format(channel_id=channel_id)), 'w')
        for x in glob(os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+"_*")):
            file.write("file '{inputfile}'\n".format(inputfile=x))
        file.close()
        return os.path.join(settings.MEDIA_ROOT, "outputs/{channel_id}.txt".format(channel_id=channel_id))

    @staticmethod
    def run_shell_command(command_line):
        command_line_args = shlex.split(command_line)
        print('Subprocess: "' + command_line + '"')
        print(command_line_args)
        try:
            command_line_process = subprocess.Popen(
                command_line,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            for l in iter(command_line_process.stdout.readline, b''):
                print(l.strip())

            command_line_process.communicate()
            command_line_process.wait()

        except (OSError, subprocess.CalledProcessError) as exception:
            print('Exception occured: ' + str(exception))
            print('Subprocess failed')
            return False
        else:
            # no exception was raised
            print('Subprocess finished')

        return True

    @staticmethod
    def merge_files(channel_id, options):
        count = 1
        for i in glob(os.path.join(settings.MEDIA_ROOT, channel_id)+"/*"):
            print(glob(i+"/*.m3u8"))
            if len(glob(i+"/*.m3u8")) == 1:
                if options['merge_mode'] in [0, 1]:
                    command = 'ffmpeg -i {input} -r {fps} -vf scale={width}:{height} {output}'.format(
                        input=glob(i+"/*.m3u8")[0],
                        fps=str(options['fps']),
                        width=str(options['width']),
                        height=str(options['height']),
                        output=os.path.join(
                            settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(count)+".mp4")
                    )
                elif options['merge_mode'] == 2:
                    command = 'ffmpeg -i {input} -r {fps} -vf scale={width}:{height} -an {output}'.format(
                        input=glob(i+"/*.m3u8")[0],
                        fps=str(options['fps']),
                        width=str(options['width']),
                        height=str(options['height']),
                        output=os.path.join(
                            settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(count)+".mp4")
                    )
                else:  # Merge Mode 3
                    command = 'ffmpeg -i {input} -r {fps} -vf scale={width}:{height} -vn {output}'.format(
                        input=glob(i+"/*.m3u8")[0],
                        fps=str(options['fps']),
                        width=str(options['width']),
                        height=str(options['height']),
                        output=os.path.join(
                            settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(count)+".m4a")
                    )
                print(command)
                Utils.run_shell_command(command)
                count += 1
        # Only 1 file is generated.
        if count == 2:
            if options['merge_mode'] == 0:
                os.rename(os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(
                    count)+".mp4"), os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".mp4"))
            elif options['merge_mode'] == 2:
                os.rename(os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(
                    count)+".mp4"), os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".mp4"))
            else:
                os.rename(os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+"_"+str(
                    count)+".m4a"), os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".m4a"))
        elif count > 2:
            input_string = Utils.get_mergable_list(channel_id)
            print(input_string)
            if options['merge_mode'] == 0:
                command = 'ffmpeg -f concat -safe 0 -i {inputs} -c copy {output}'.format(
                    inputs=input_string, output=os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".mp4"))
            elif options['merge_mode'] == 2:
                command = 'ffmpeg -f concat -safe 0 -i {inputs} -c copy {output}'.format(
                    inputs=input_string, output=os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".mp4"))
            else:
                command = 'ffmpeg -f concat -safe 0 -i {inputs} -c copy {output}'.format(
                    inputs=input_string, output=os.path.join(settings.MEDIA_ROOT, "outputs/"+channel_id+".m4a"))
            Utils.run_shell_command(command)
        return True

    @staticmethod
    def process(channel_id, options):
        channel = ChannelStatus.objects.filter(channel_id=channel_id)
        presigned_url = ''
        if not channel.exists():
            channel = ChannelStatus(channel_id=channel_id, status='Queued')
            channel.save()
            bg_process.delay(channel_id, options)
        else:
            channel = channel[0]
            if channel.status == 'Completed':
                s3 = boto3.client('s3',
                                  region_name='ap-south-1',
                                  aws_access_key_id=settings.AWS_ACCESS_KEY,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY, config=Config(signature_version='s3v4'))
                presigned_url = s3.generate_presigned_url('get_object', Params={
                                                          'Bucket': settings.AWS_OUTPUT_BUCKET_NAME, 'Key': channel.aws_key}, ExpiresIn=60*24)
                print(presigned_url)
        return {
            "status": channel.status,
            "created_at": channel.created_at,
            "updated_at": channel.last_updated_at,
            "presigned_url": presigned_url
        }
