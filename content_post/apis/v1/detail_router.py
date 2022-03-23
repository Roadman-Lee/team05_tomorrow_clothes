from typing import Any, Dict, List

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ninja import File, Form, Router, UploadedFile

from content_post.apis.v1.schemas.detail_response import CommentResponse, DetailResponse
from content_post.apis.v1.schemas.schema_test import UserSchema
from content_post.models.contents import Comments, Feeds
from user_admission.models.user import User

content = Router(tags=["Content_CRUD"])




# detail/feeds page render router
@content.get("/feeds/", response=DetailResponse)
@login_required(login_url="/login/")
def get_feeds_page(request: HttpRequest) -> HttpResponse:
    return render(request, "add.html")


# 상세 FEED페이지로 이동
@content.get("/{feed_id}/", response=List[DetailResponse])
def get_detail_page(request: HttpRequest, feed_id: int) -> HttpResponse:
    user_id = request.user.id
    # 로그인된 유저의 아이디값
    feed = Feeds.objects.get(id=feed_id)
    # 디테일 페이지에 뿌려질 피드 객체
    check = feed.scrape.filter(id=user_id)  # type: ignore
    # 로그인된 유저의 값으로 피드에 스크랩했는지 체크
    comments = Comments.objects.filter(feed_id=feed_id).order_by("-created_at")
    # 피드에 달린 댓글 객체들
    if check.exists():
        # 만약 스크랩을 했다면
        return render(
            request,
            "detail.html",
            {"feed": feed, "comments": comments, "scraped": "scraped"},
        )
    else:
        # 스크랩을 안했다면
        return render(request, "detail.html", {"feed": feed, "comments": comments})


# # 수정페이지 이동 변경예정 효정님 _______________


# detail/feeds/ (추가)
@content.post("/feeds/", response=DetailResponse)
@login_required(login_url="/login/")
def post_feeds_page(
        request: HttpRequest,
        feeds_comment: str = Form(...),
        feeds_img_url: UploadedFile = File(...),
) -> HttpResponse:
    writer = get_object_or_404(User, id=request.user.id)
    Feeds.objects.create(
        feeds_comment=feeds_comment, feeds_img_url=feeds_img_url, writer=writer
    )
    feed_id = Feeds.objects.order_by("-id")[0].id
    return redirect("/detail/" + str(feed_id) + "/")


# detail/feeds/<int:feed_id> 수정
@content.post("/feeds/update/{feed_id}/")
def put_feeds_page(
        request: HttpRequest,
        feed_id: int,
        feeds_comment: str,
        feeds_img_url: UploadedFile,
) -> Dict[str, str]:

    new_feed = Feeds.objects.get(id=feed_id)  # type:ignore
    new_feed.feeds_comment = feeds_comment
    new_feed.feeds_img_url = feeds_img_url
    new_feed.save()
    return redirect(f"/detail/{feed_id}/")
    # return {"msg": "수정 완료"}


# detail/feeds/<int:feed_id> 삭제
@content.post("/feeds/delete/{feed_id}", response=DetailResponse)
def delete_feeds_page(request: HttpRequest, feed_id: int) -> HttpResponse:
    delete_feed = get_object_or_404(Feeds, id=feed_id)
    delete_feed.delete()
    return redirect("test_1:login")

# 수정페이지 이동 변경예정
