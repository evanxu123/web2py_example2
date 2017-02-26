# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index1():
    """
    lets users login or logout
    """
    # for development purposes only:
 
    print auth.user_id
    
    return dict()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.post)
    return locals()

def index():
    """
    lets users login or logout
    """
    response.flash = 'how to use this website: first you need to logout to homepage you will only see the post but cannot edit it. When you creat your account you can publish and edit it. This website also have a manager model but you can not access it. It need my email and password.'
    form = SQLFORM(db.post).process()
    rows = db(db.post).select()
    # for development purposes only:
    print "user_id: %s" % auth.user_id
    
    posts = get_posts()
    
    # most recent post:
    last_post = posts.first()
    
    # oldest post:
    first_post = posts.last()
    
    # number of posts:
    post_count = len(posts)

    print "post_count: %s" % post_count
    return locals()
    #return dict(last_post=last_post, first_post=first_post, post_count=post_count)

def get_posts():
    """get posts, in reverse chronological order"""
    return db(db.post).select().sort(lambda p: p.updated_on, reverse=True)

@auth.requires_login()
def create_post():
    """form for posting a  new comment"""
    form = SQLFORM(db.post, 
                 labels= {'post_subject': "Subject", 'post_content': "Comment"},
                 submit_button = 'Submit your comment',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'comment accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please post your comment'

    return dict(form=form)

@auth.requires_login()
def edit_post():
    """form for editing an existing post"""
    post = db.post[request.args(0)]
    if not(post and post.user_id == auth.user_id):
        redirect(URL('index'))
    form = SQLFORM(db.post, post,
                 labels= {'post_subject': "Subject", 'post_content': "Comment"},
                 showid= False,
                 deletable= True,
                 submit_button = 'Update your comment',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'comment accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please edit your comment'

    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
