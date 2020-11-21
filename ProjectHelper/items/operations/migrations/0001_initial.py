# Generated by Django 2.2 on 2020-11-21 22:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('comments', models.CharField(max_length=200, verbose_name='评论内容')),
            ],
            options={
                'verbose_name': '项目评论',
                'verbose_name_plural': '项目评论',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('tag', models.CharField(max_length=50, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签清单',
                'verbose_name_plural': '标签清单',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '组队申请',
                'verbose_name_plural': '组队申请',
            },
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('comments', models.CharField(max_length=200, verbose_name='评论内容')),
            ],
            options={
                'verbose_name': '队伍评论',
                'verbose_name_plural': '队伍评论',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('lab', models.CharField(max_length=1, verbose_name='实验班名称')),
            ],
            options={
                'verbose_name': '课程清单',
                'verbose_name_plural': '课程清单',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '组队情况',
                'verbose_name_plural': '组队情况',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('message', models.CharField(max_length=200, verbose_name='消息内容')),
                ('is_read', models.BooleanField(default=False, verbose_name='消息是否已读取')),
            ],
            options={
                'verbose_name': '消息记录',
                'verbose_name_plural': '消息记录',
            },
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operations.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '用户标签',
                'verbose_name_plural': '用户标签',
            },
        ),
    ]
