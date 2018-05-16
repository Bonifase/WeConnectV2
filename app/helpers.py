from app import app


""""cleans the user json data"""

def clean_data(**user):
	cleaned_data = {}
	for key in user:
		if user[key] is None:

			assert False, key + 'is missing'
		else:
			cleaned_data[key] = str(user[key])
			
	return cleaned_data

"""cleans the business json data"""

def business_data(**business):
	business_data = {}
	for key in business:
		if business[key] is None:

			assert False, key + ' key is missing'
		else:
			business_data[key] = str(business[key])
			
		
	return business_data
	
def search(search_params):
    search = search_params.get('q')
    operator = "%" + search + "%"
    subquery = Business.query.filter(Business.name.ilike(operator))
                            # .filter(Business.description.ilike(operator))\
                            # .filter(Business.category.ilike(operator))\
                            # .filter(Business.location.ilike(operator))

    limit = search_params.get('limit')
    page = search_params.get('page')
    subquery = business_pagination(subquery, limit, page)
    return subquery.all()

def filter(filter_params):
    """" This method filter business by name, location and category"""
    subquery=Business.query
    required_fields = ['location', 'name', 'category']
    for filter in filter_params:
        if filter not in required_fields:
            continue
        operator = "%" + filter_params[filter] + "%"
        subquery = subquery.filter(getattr(Business, filter).ilike(operator))


"""ROUTES FOR THE VIEWS"""
def register_user():

	register_route = app.route('/api/v2/auth/register', methods=['POST'])
	return register_route

""""LOGIN ROUTE"""
def login():
	login_user = app.route('/api/v2/auth/login',  methods=['POST'])
	return login_user


""""LOGIN ROUTE"""
def login():
	login_user = app.route('/api/v2/auth/login',  methods=['POST'])
	return login_user

""""RESET PASSWORD ROUTE"""
def reset_password():
	reset_password = app.route('/api/v2/auth/reset-password', methods=['POST'])
	return reset_password

""""CONFIRM RESET PASSWORD ROUTE"""
def confirm_reset_password():
	confirm_reset_password = app.route('/api/v2/auth/reset-password/<string:reset_token>', methods=['POST'])
	return confirm_reset_password

""""LOGOUT ROUTE"""
def logout():
	logout_user = app.route('/api/v2/auth/logout', methods=['POST'])
	return logout_user

	""""CREATE BUSINESS ROUTE"""
def create_business():
	create_business = app.route('/api/v2/businesses', methods=['POST'])
	return create_business

"""RETRIEVE ALL BUSINESSES ROUTE"""
def retrieve_all():
	retrieve_all = app.route('/api/v2/businesses', methods=['GET'])
	return retrieve_all

""""RETIEVE WITH PAGINATION ROUTE"""
def retrieve_with_pagination():
	pagination = app.route('/api/v2/businesses/<int:page_num>', methods = ['GET'])
	return pagination

""""RETRIEVE ONE BUSINESS ROUTE"""
def retrieve_business_by_id():
	retrieve_one = app.route('/api/v2/businesses/<int:id>/', methods=['GET'])
	return retrieve_one

""""UPDATE BUSINESS ROUTE"""
def update_business():
	update_business = app.route('/api/v2/businesses/<int:id>', methods=['PUT'])
	return update_business

""""DELETE BUSINESS ROUTE"""
def delete_business():
	delete_business = app.route('/api/v2/businesses/<int:id>', methods=['DELETE'])
	return delete_business

"""SEARCH BUSINESS ROUTE"""
def search_business():	
	search = app.route('/api/v2/businesses/search', methods = ['GET'])
	return search

	""""ADD BUSINESS REVIEW ROUTE"""
def add_business_review():
	add_review = app.route('/api/v2/<int:businessid>/reviews', methods=['POST'])
	return add_review

	""""RETRIEVE BUSINESS REVIEWS ROUTE"""
def retrieve_all_business_reviews():
	get_reviews = app.route('/api/v2/<int:businessid>/reviews', methods=['GET'])
	return get_reviews

	
