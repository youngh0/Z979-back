from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .dto.feed_update_dto import FeedUpdateDto
from .dto.feed_read_dto import SpecificFeedDto
from .serializers import FeedSerializer
from .models import Feed
from challenge.models import Challenge
from .dto import feed_update_dto
from django.core import serializers
import json

# 피드 작성
@api_view(['POST'])
def post_feed(request, user_id):
    # User객체 찾아오는 코드 필요

    #
    serializer = FeedSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        challenge_info = Challenge.objects.get(id=request.data['challenge'])
        serializer.validated_data['challenge'] = challenge_info
        serializer.save()

        feed_info = Feed.objects.get(id=1)
        data = {
            "content" : feed_info.content,
            "hashtags" : feed_info.hashtags
        }

        return Response({"data" : data}, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse("post fail", status=status.HTTP_400_BAD_REQUEST)

# 피드 수정
@api_view(['PUT'])
def update_feed(request, user_id, feed_id):


    # User객체 찾아오는 코드 필요
    base_feed = Feed.objects.get(pk=1)


    base_feed.content = request.data['content']
    base_feed.hashtags = request.data['hashtags']

    base_feed.save()

    update_feed_info = Feed.objects.get(pk=1)

    res_feed_data = json.dumps(FeedUpdateDto(update_feed_info.content, update_feed_info.hashtags).__dict__)

    return Response({
        "data" : res_feed_data
    }, status = status.HTTP_200_OK)


# 피드 전체보기
# TODO : 닉네임 부분 실제 user객체의 닉네임으로 수정해야함
@api_view(['GET'])
def all_feed_list(request):
    feed_list = Feed.objects.all()
    res_data = []

    for feed in feed_list:
        feed_dto =SpecificFeedDto("cha", feed.content, feed.hashtags, feed.like, feed.is_challenge)
        res_data.append(feed_dto.__dict__)

    return Response({"feed_cnt" : len(res_data),"data":res_data}, status=status.HTTP_200_OK)

# 챌린지 피드 모아보기
# TODO : 닉네임 부분 실제 user객체의 닉네임으로 수정해야함
@api_view(['GET'])
def find_challenge_feed(request):
    all_feed = Feed.objects.all()
    res_data = []

    for feed in all_feed:
        if feed.is_challenge:
            feed_dto = SpecificFeedDto("cha", feed.content, feed.hashtags, feed.like, feed.is_challenge)
            res_data.append(feed_dto.__dict__)

    return Response({"feed_cnt": len(res_data), "data": res_data}, status=status.HTTP_200_OK)

# 좋아요 누르기
@api_view(['PUT'])
def like_feed(request, feed_id):
    feed = Feed.objects.get(id= feed_id)
    feed.like += 1
    if feed.like >= 5:
        # 스탬프 부여 코드
        print(end="")

    feed.save()

    res_data = Feed.objects.get(id=feed_id)

    return Response({'like': res_data.like}, status=200)

# 챌린지 별 피드 좋아요 순
@api_view(['GET'])
def find_challenge_feed_orderby_like(request,challenge_id):
    all_feed = Feed.objects.all()
    res_data = []

    for feed in all_feed:
        if feed.is_challenge:
            if feed.challenge.id == challenge_id:

                feed_dto = SpecificFeedDto("cha", feed.content, feed.hashtags, feed.like, feed.is_challenge)
                res_data.append(feed_dto.__dict__)

    res_data.sort(key=lambda x : x['like'], reverse=True)

    return Response({"feed_cnt" : len(res_data),"data":res_data},status=status.HTTP_200_OK)

# 캠페인 피드 모아보기

# 피드 삭제

# 내 글 모아보기