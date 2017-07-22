# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from datetime import datetime

def index():
    form = FORM(INPUT(_name='search_phrase', _class="search_input", requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _class="search_button", _value='Search UNT'), _method='GET')
    if session.ii is None:
        session.ii=search().invertIndexDocs()
    if request.vars.search_phrase is not None:
        search_txt = request.vars.search_phrase
        redirect(URL('search_text', vars=dict(search_txt=search_txt)))
    return dict(form=form)

def search_text():
    search_txt=request.vars['search_txt']
    if search_txt is None:
        search_txt=request.vars.q
        if search_txt is None:
            redirect(URL('index'))

    page = request.vars.page
    if page is None:
        page=0
    try:
        page=int(page)
    except:
        page=0
    print "page is", page

    form = FORM(INPUT(_name='search_phrase', _class="search_input",_value=search_txt, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _class="search_button", _value=''), _action='index', _method='GET')
    results_disp=None
    if session.ii is None:
        print "Indexing.."
        session.ii=search().invertIndexDocs()
    #results=session.results
    results=None
    t1 = datetime.now()
    if results is None:
        print "retreiving"
        results=search().search_for_text(session.ii,search_txt)
        session.results=results
    
    #pagination code starts here
    total_links = len(results)
    links_per_page = 10
    num_pages = total_links / links_per_page  # ceil(100/10) = 10 pages
    cur_page = page

    start = page * links_per_page
    end = start + links_per_page
    if end > total_links: # false
      end = total_links

    results_disp = results[start:end]

    #results_disp=results[:10]

    #return dict(form=form,results_disp=results_disp,prev=None,nxt=nxt)
    t2 = datetime.now()
    delta = t2 - t1
    time_retr=delta.seconds + delta.microseconds/1E6
    return dict(
      form=form,
      q=search_txt,
      num_results=total_links,
      time_retr=time_retr,
      results_disp=results_disp,
      num_pages=num_pages,
      prev=page-1 if page > 0 else None, # set to None if page =0
      nxt=page+1 if page < num_pages else None, # set to None if page == num_pages
    )

def show_items():
    results=session.results
    total_links = len(results)
    page = int(request.vars.page)
    query = request.vars.q
    links_per_page = 10
    num_pages = total_links / links_per_page  # ceil(100/10) = 10 pages
    print 'num_pages', num_pages
    cur_page = page

    start = page * links_per_page
    end = start + links_per_page
    if end > total_links: # false
      end = total_links

    results_disp = results[start:end] # this page's items

    form = FORM('Search :',INPUT(_name='search_phrase',_value=query, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit',_value='Search'),_action='index', _method='GET')

    return dict(
      results_disp=results_disp,
      prev=page-1 if page > 0 else None, # set to None if page =0
      next=page+1 if page < num_pages else None, # set to None if page == num_pages
    )

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


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
