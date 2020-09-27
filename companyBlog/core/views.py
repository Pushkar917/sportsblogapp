from flask import render_template, Blueprint, request, url_for, redirect

from companyBlog import cache
from companyBlog.models import BlogPosts
import stripe

core = Blueprint('core', __name__)

public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


@core.route('/')
@cache.cached(timeout=2)
def index():
    '''This is the home page'''
    '''It limits the no of post to be shown in a page'''
    ''' Limits the query size by calling paginate'''

    page = request.args.get('page', 1, type=int)
    blogposts = BlogPosts.query.order_by(BlogPosts.timeofPost.desc()).paginate(page=page, per_page=5)
    next_url = url_for('core.index', posts=blogposts, page=blogposts.next_num) \
        if blogposts.has_next else None
    prev_url = url_for('core.index', posts=blogposts, page=blogposts.next_num) \
        if blogposts.has_prev else None
    return render_template('index.html', posts=blogposts, next_url=next_url, prev_url=prev_url)


@core.route('/subscribe')
def subscribe():
    '''This is about passing the info of the page'''
    return render_template('subscribe.html', public_key=public_key)


@core.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")


@core.route('/payment', methods=['POST'])
def payment():
    # customerInfo
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])
    # PaymentInformation
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=99,
        currency='usd',
        description='Subscription for news letter'
    )
    return render_template("newsletter.html")
