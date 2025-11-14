from minio import Minio

from django.core.management.base import BaseCommand


def add_images():
    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', 'comedyclub.png', "app/static/images/comedyclub.png")
    client.fput_object('images', 'got.png', "app/static/images/got.png")
    client.fput_object('images', 'it.png', "app/static/images/it.png")
    client.fput_object('images', 'metro2033.png', "app/static/images/metro2033.png")
    client.fput_object('images', 'office.png', "app/static/images/office.png")
    client.fput_object('images', 'mrbeast.png', "app/static/images/mrbeast.png")

    print("Картинки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_images()









