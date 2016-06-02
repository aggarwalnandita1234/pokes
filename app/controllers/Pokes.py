"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Pokes(Controller):
    def __init__(self, action):
        super(Pokes, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('Poke')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):

        return self.load_view('index.html')
    def dashboard(self):
        info=session['id']
        users=self.models['Poke'].get_users(info)
        get_pokes=self.models['Poke'].get_pokes(info)
        get_total_pokes=self.models['Poke'].get_total_pokes(info)
        return self.load_view('dashboard.html', users=users, get_pokes=get_pokes, get_total_pokes=get_total_pokes[0])
    def logout(self):
        session.clear()
        return redirect('/')
    def create(self):
        
        user_info = {
             "name" : request.form['form-first-name'],
             "alias": request.form['form-last-name'],
             "email": request.form['form-email'],
             "password":request.form['form-password'],
             "pw_confirmation" : request.form['form-conf-password']
        }


        create_status = self.models['Poke'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']  
            return redirect('/dashboard')
        else:

            for message in create_status['errors']:
                flash(message, 'regis_errors')

            return redirect('/')

    def login(self):

        user_info = {
            "email" : request.form['form-email'],
            "password" : request.form['form-password']
        }
        print "before calling create_status"
        create_status = self.models['Poke'].login(user_info)
        print "after calling create_status"
        if create_status['status'] == True:
            print "we are in create_status=True"
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['name']
            print session['id']
            return redirect('/dashboard')
        else:

            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def poke(self, id):
        pokes=int(request.form['pokes'])
        pokes=pokes+1
        print "THIS IS FORST PRINT", pokes
        info={
            'id':id,
            'pokes':pokes,
            'poked_by':session['id']}
        users=self.models['Poke'].update_poke(info)
        add_poke=self.models['Poke'].add_poke(info)

        return redirect('/dashboard')










