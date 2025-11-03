@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(status=400, message='Email and password required'), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify(status=409, message='Email already exists'), 409
    
    new_user = User(
        email=data['email'],
        role='employee',  # Défaut pour guest
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(status=201, data=new_user.to_dict(), message='Account created'), 201