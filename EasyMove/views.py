from django.shortcuts import render,redirect
from django.contrib import messages
from .models import EasyMoveItem, UserInfo, Comment, User
from actions.models import Action
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
import requests
import json


# Create your views here.

def home(request):
    items = EasyMoveItem.objects.all().order_by('-date_posted')
    if request.session.get("username", False):
        user = User.objects.get(username=request.session.get("username"))

        user_upload = EasyMoveItem.objects.all().filter(user_id=user.id)
        actions_user = Action.objects.all().filter(user_id=user.id)
        actions_target_user = Action.objects.all().filter(target_id=user.id,target_ct=ContentType.objects.get_for_model(User))
        action_target_item = Action.objects.all().filter(target_id__in=user_upload,target_ct=ContentType.objects.get_for_model(EasyMoveItem))

        actions = actions_user|actions_target_user|action_target_item
        actions = actions.order_by("-date_created")[:5]

        return render(request,
                      "EasyMove/home.html",
                      {"items": items, "actions":actions}
                      )
    else:
        return render(request,
                      "EasyMove/home.html",
                      {"items": items}
                      )


def easy_move_list(request):
    items = EasyMoveItem.objects.all().order_by('-date_posted')
    actions = Action.objects.all()
    return render(request,
              "EasyMove/easy_move/list.html",
              {"items": items, "actions":actions}
              )



def easy_move_items_detail(request, item_id):
    item = EasyMoveItem.objects.get(id=item_id)
    comments = Comment.objects.filter(item_id=item_id).order_by('-date_posted')
    return render(request,
                  "EasyMove/easy_move/detail.html",
                  {"item": item, "comments": comments},
                  )



def easy_move_add_item(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    if request.method == 'POST':
        # process the form
        title = request.POST.get("add-title")
        price = request.POST.get("add-price")
        condition = request.POST.get("add-condition")
        description = request.POST.get("description")
        availability = request.POST.getlist("add-availability")
        location = request.POST.get("add-location")
        item_img = request.FILES["item_image"]

        if title.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The title is invalid/empty, please try again.")
            return redirect("EasyMove:add-item")

        if condition.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The condition is invalid/empty, please try again.")
            return redirect("EasyMove:add-item")

        if description.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The description is invalid/empty, please try again.")
            return redirect("EasyMove:add-item")

        if location.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The location is invalid/empty, please try again.")
            return redirect("EasyMove:add-item")


        option = '/'.join(availability)
        if option == '':
            messages.add_message(request, messages.ERROR,
                                 "Please select at least one availability option.")
            return redirect("EasyMove:add-item")


        endpoint = "https://easymovevision.cognitiveservices.azure.com/vision/v3.1/analyze"
        parameters = {
            'visualFeatures':'Adult'
        }
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '4d013d6596ad47f3af39739e0699742b',
        }
        response = requests.post(endpoint,headers=headers, params=parameters,data=item_img)
        result = response.json()
        if result['adult']['isAdultContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains adult content,please change it.")
            return redirect("EasyMove:add-item")

        if result['adult']['isRacyContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains racy content,please change it.")
            return redirect("EasyMove:add-item")

        if result['adult']['isGoryContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains gory content,please change it.")
            return redirect("EasyMove:add-item")

        user = User.objects.get(username=request.session.get("username"))

        new_item = EasyMoveItem(
            title=title,
            price = price,
            condition = condition,
            description = description,
            availability = option,
            location = location,
            author=request.session.get('username'),
            user=user,
            item_img = item_img
        )
        new_item.save()


        action=Action(
            user=user,
            verb="created the new item",
            target=new_item
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "You successfully submitted the new item: %s" %new_item.title )

        return redirect("EasyMove:item-detail", new_item.id)

    else:
        # show the form
        # messages.add_message(request, messages.WARNING, "Failed add the item, try add again")
        return render(request,
                      "EasyMove/easy_move/add.html",
                      )



def easy_move_edit_item(request, item_id):
    editing_item = EasyMoveItem.objects.get(id=item_id)

    return render(request,
                  "EasyMove/easy_move/edit.html",
                  {"item": editing_item}
                  )


def easy_move_submit_edit(request, item_id):

    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    editing_item = EasyMoveItem.objects.get(id=item_id)

    if request.method == 'POST':
        # process the form

        title = request.POST.get("add-title")
        price = request.POST.get("add-price")
        condition = request.POST.get("add-condition")
        description = request.POST.get("description")
        availability = request.POST.getlist("add-availability")
        location = request.POST.get("add-location")

        if title.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The title is invalid/empty, please try again.")
            return redirect("EasyMove:edit-item", item_id)

        if condition.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The condition is invalid/empty, please try again.")
            return redirect("EasyMove:edit-item", item_id)

        if description.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The description is invalid/empty, please try again.")
            return redirect("EasyMove:edit-item", item_id)

        if location.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The location is invalid/empty, please try again.")
            return redirect("EasyMove:edit-item", item_id)

        option = '/'.join(availability)
        if option == '':
            messages.add_message(request, messages.ERROR,
                                 "Please select at least one availability option.")
            return redirect("EasyMove:edit-item", item_id)

        # update information
        editing_item.title = title
        editing_item.price = price
        editing_item.condition = condition
        editing_item.description = description
        editing_item.availability = option
        editing_item.location = location

        # save update
        editing_item.save()

        user = User.objects.get(username=request.session.get("username"))
        # log the action
        action = Action(
            user=user,
            verb="edited the item",
            target=editing_item
        )
        action.save()

        messages.add_message(request, messages.INFO, "You successfully edited the item %s" %editing_item.title)

        return redirect("EasyMove:item-detail", item_id)
    else:
        # messages.add_message(request, messages.WARNING, "Failed edit the item %s" %editing_item.title)
        return redirect("EasyMove:item-detail", item_id)



def easy_move_delete_item(request, item_id):
    # check if user logged in
    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    title = EasyMoveItem.objects.get(pk=item_id).title

    EasyMoveItem.objects.get(pk=item_id).delete()
    messages.add_message(request, messages.WARNING, "You successfully deleted the item %s" %title)
    return redirect("EasyMove:easy-move-list")



def easy_move_change_location(request):
    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            user = User.objects.get(username=request.session.get('username'))
            user.location = request.POST.get('new_location')
            user.save()
            return JsonResponse({'success':'success', 'new_location':user.location}, status=200)

        except UserInfo.DoesNotExist:
          #  if user not exist
            return JsonResponse({'error': 'No user found with that username'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)



def easy_move_item_compare(request, item_id):
    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        item_title = request.POST.get('item_title')
        try:
            similar_item = EasyMoveItem.objects.exclude(pk=item_id).filter(title__icontains=item_title)
            if similar_item:
                similar_item = similar_item[0]
                similar_item_id = similar_item.id
                similar_item_price = similar_item.price
                return JsonResponse({'success':'success', 'similar_item_price':similar_item_price, 'similar_item_id':similar_item_id}, status=200)
            else:
                return JsonResponse({'error': 'No similar found'}, status=200)

        except UserInfo.DoesNotExist:
          #  if user not exist
            return JsonResponse({'error': 'No similar found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)



def new_comment_add(request):
    if not request.session.get("username", False):
        return redirect('EasyMove:easy-move-home')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        commentTitle = request.POST.get('title')
        commentText = request.POST.get('comment')
        item_id = request.POST.get('item_id')
        user = User.objects.get(username=request.session.get("username"))

        if commentTitle =='':
            return JsonResponse({'error': 'Comment title is required.'}, status=200)
        elif commentText =='':
            return JsonResponse({'error': 'Comment is required.'}, status=200)

        try:
            item = EasyMoveItem.objects.get(pk=item_id)

            new_comment = Comment(
                author=request.session.get('username'),
                user=user,
                commentTitle=commentTitle,
                commentText=commentText,
                item=item
            )
            new_comment.save()

            # log the action
            action = Action(
                user=user,
                verb="added a new comment for item",
                target= item
            )
            action.save()

            # Find how many comment left for this item
            comment_length = Comment.objects.filter(item_id=item.id).count()

            return JsonResponse({'success':'success',"comment_length":comment_length,"comment_id":new_comment.id}, status=200)
        except EasyMoveItem.DoesNotExist:
            return JsonResponse({'error':'No item found with item ID.'}, status=200)

    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


def update_user_role(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        new_role = request.POST.get('new_role')
        user.details.role = new_role
        user.save()
        if(username == request.session.get("username")):
            request.session['role'] = user.details.role
        print(request.session['role'])

        action_user = User.objects.get(username=request.session.get("username"))
        # log the action
        action = Action(
            user= user,
            verb="'s role has been changed to "+new_role + " by administrator ",
            target = action_user
        )
        action.save()


        return JsonResponse({'success':'success','currentRole':request.session['role']},status=200)
    else:
        return JsonResponse({'error':'Invalid Ajax request'}, status=400)

def delete_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        item = comment.item

        user = User.objects.get(username=request.session.get("username"))
        action = Action(
            user=user,
            verb="just deleted a comment for item ",
            target = item
        )
        action.save()
        comment.delete()

        # Find how many comment left for this item
        comment_length = Comment.objects.filter(item_id=item.id).count()

        return JsonResponse({'success': 'success',"comment_length":comment_length}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)

def edit_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    print(is_ajax)

    if is_ajax and request.method == "POST":
        comment_id = request.POST.get('comment_id')
        updated_title = request.POST.get('updated_title')
        updated_content = request.POST.get('updated_content')
        comment = Comment.objects.get(id=comment_id)
        comment.commentTitle = updated_title
        comment.commentText = updated_content
        comment.save()

        user = User.objects.get(username=request.session.get("username"))
        action = Action(
            user=user,
            verb="edited the comment for item ",
            target=comment.item
        )
        action.save()

        return JsonResponse({'success': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


def item_search(request):
    if request.method == 'GET':
        search_query = request.GET['search']

    search_results = EasyMoveItem.objects.filter(title__icontains=search_query)

    return render(request,
                  "EasyMove/easy_move/searchResult.html",
                  {"items": search_results}
                  )






















