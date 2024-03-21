from flask import Blueprint, render_template,request,flash, jsonify
from flask_login import login_required, current_user

from .models import User, Note
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method =="POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short',category='error')
        else:
            new_note = Note(data=note,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')


    
    return render_template('home.html',user=current_user)


@views.route('/admin_home',methods=['GET','POST'])
def admin_home():
    users = User.query.filter(User.first_name != 'admin').all()
    return render_template('admin_home.html',user=current_user, user_list = users)

@views.route('/delete-user', methods=['POST'])
def delete_user():
    data = json.loads(request.data)
    user_id = data['userId']
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
            
    
    return jsonify({}) 

@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    
    return jsonify({}) 


