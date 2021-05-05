from enum           import unique
from flask_login    import UserMixin
from . import db

class User(db.Model, UserMixin):
    #Attribute Columns
    id       = db.Column(db.Integer,     primary_key=True) 

    email    = db.Column(db.String(75) , nullable= True, unique= True) 
    username = db.Column(db.String(50) , nullable= False) 
    password = db.Column(db.String(100), nullable= True ) 
    rank     = db.Column(db.Integer    , nullable= False)

    #Relationships:
    notes = db.relationship("Notes", backref="user_object", lazy=True)

    #A method used to check password during login 
    def check_password(self, password1):    	
        return password1 == self.password

    #A method that returns the Primary key, This in used in the "load_user" function in routes.spy
    def get_id(self):
            #return (self.email).encode('utf-8')   #str.encode returns 'bytes' object
            return self.id

    #A method that prints the reffered user instance
    def __repr__(self):
        #return self
    	#return f'"<User {self.id}>"'         #"<User {}>".format(self.id)
    	return f'Email: {self.email}, Username: {self.username}, Password: {self.password}'


 class Person(db.Model):
     __tablename__ = 'person'

    #Attribute Columns
    id              = db.Column(db.Integer    , primary_key=True)
    name            = db.Column(db.String(75) , nullable=False)
    cnic            = db.Column(db.String(16) , nullable=False, unique=True)
    phone           = db.Column(db.String(11) , nullable=False, unique=True)
    email           = db.Column(db.String(100), nullable=False, unique=True)
    cnic_front      = db.Column(db.String(500), nullable=False)
    cnic_back       = db.Column(db.String(500), nullable=False)
    comments        = db.Column(db.Text       , nullable=True, default=db.null())

    #Relationships
    buyer           = db.relationship('Buyer'           , backref='person', lazy=True)
    commissionagent = db.relationship('CommissionAgent' , backref='person', lazy=True)
    user            = db.relationship('User'            , backref='person', lazy=True)

     @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'cnic': self.cnic,
            'phone': self.phone,
            'email': self.email,
            

        }



class Buyer(db.Model):
    __tablename__ = 'buyer'

    #Attribute Columns
    # id           = db.Column(db.Integer,     primary_key=True)
    # name         = db.Column(db.String(75) , nullable=False)
    # cnic         = db.Column(db.String(16) , nullable=False, unique=True)
    # phone        = db.Column(db.String(11) , nullable=False, unique=True)
    # email        = db.Column(db.String(100), nullable=False, unique=True)
    address      = db.Column(db.String(100), nullable=False)
    # cnic_front   = db.Column(db.String(500), nullable=False)
    # cnic_back    = db.Column(db.String(500), nullable=False)
    # comments     = db.Column(db.Text,        nullable=True,  default=db.null())

    #Foregin Key Columns
    person_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)

    #Relationships:
    deals = db.relationship("Deal", backref='buyer_object', lazy=True)
    files = db.relationship("File", backref="buyer_object" , lazy=True)

    @property
    def serialize(self):
        return {
            'id'       : self.id,               
            'name'     : self.name,
            'cnic'     : self.cnic,
            'comments' : self.comments,
            'deals'    : [deal.serialize for deal in self.deals],
            'files'    : [file.serialize for file in self.files]
        }
    

class CommissionAgent(db.Model):
    __tablename__ = 'commissionagent'

    #Attribute Columns:
    id              = db.Column(db.Integer    , primary_key=True)
    name            = db.Column(db.String(75) , nullable=False)
    cnic            = db.Column(db.String(16) , nullable=False, unique=True)
    phone           = db.Column(db.String(11) , nullable=False, unique=True)
    email           = db.Column(db.String(100), nullable=False, unique=True)
    cnic_front      = db.Column(db.String(500), nullable=False)
    cnic_back       = db.Column(db.String(500), nullable=False)
    comments        = db.Column(db.Text       , nullable=True, default=db.null())

    #Relationships:
    #This attribute returns a list of deals that  are associated to a particular agent, when called
    deals = db.relationship("Deal", backref='working_agent_object', lazy=True)

    @property
    def serialize(self):
        '''
        Return object data in easily serializable format
        '''
        return {
            'id'              : self.id,               
            'name'            : self.name,
            'cnic'            : self.cnic,
            'phone'           : self.phone,
            'email'           : self.email,
            'comments'        : self.comments,
        }

class Plot(db.Model):
    __tablename__ = 'plot'

    #Attribute Columns:
    id       = db.Column(db.Integer,     primary_key=True)

    type     = db.Column(db.String(100), nullable=False)
    address  = db.Column(db.String(100), nullable=False)
    status   = db.Column(db.String(20),  nullable=False)
    price    = db.Column(db.Integer,     nullable=True)
    size     = db.Column(db.String(20),  nullable=False)    
    comments = db.Column(db.Text,        nullable=True, default=None)

    #Relationships:
    #This attribute would return the deal obect this plot is associated to
    deal = db.relationship("Deal", backref='plot_object', uselist=False)

    @property
    def serialize(self):
        '''
        Return object data in easily serializable format
        '''
        return {
            'id'       : self.id,               
            'type'     : self.type,
            'address'  : self.address,
            'status'   : self.status,
            'price'    : self.price,
            'size'     : self.size,
            'comments' : self.comments,
            'deal'     : self.deal.serialize if self.deal else None
        }


class Deal(db.Model):
    __tablename__ = 'deal'

    #buyer_object = None

    #Attribute Columns:
    id                     = db.Column(db.Integer     , primary_key=True)
    status                 = db.Column(db.String(20)  , nullable=False)
    signing_date           = db.Column(db.String(20)  , nullable=False)
    amount_per_installment = db.Column(db.Integer     , nullable=True, default=db.null())
    installment_frequency  = db.Column(db.String(20)  , nullable=True, default=db.null())
    commission_rate        = db.Column(db.Float       , nullable=True, default=db.null())
    comments               = db.Column(db.Text        , nullable=True, default=db.null())

    #ForeginKey Columns:
    commission_agent_id = db.Column(db.Integer, db.ForeignKey('commissionagent.id'), nullable=True,  default=db.null())
    buyer_id            = db.Column(db.Integer, db.ForeignKey('buyer.id'),           nullable=False)
    plot_id             = db.Column(db.Integer, db.ForeignKey('plot.id'),            nullable=False, unique=True)

    #Relationships:
    transactions = db.relationship("Transaction", backref="deal_object", lazy=True)
    files        = db.relationship("File"       , backref="deal_object", lazy=True)

    @property
    def serialize(self):
        '''
        Return object data in easily serializable format
        '''
        return {
            'id'                     : self.id,               
            'status'                 : self.status,
            'signing_date'           : self.signing_date,
            'amount_per_installment' : self.amount_per_installment,
            'installment_frequency'  : self.installment_frequency,
            'commission_agent_id'    : self.commission_agent_id if self.commission_agent_id else None,
            'buyer_id'               : self.buyer_id,
            'plot_id'                : self.plot_id,
            'comments'               : self.comments
        }


class Transaction(db.Model):
    __tablename__ = 'transaction'

    #Attribute Columns:
    id        = db.Column(db.Integer , primary_key=True)
    
    amount    = db.Column(db.Integer , nullable= False)
    date_time = db.Column(db.DateTime, nullable= False)
    comments  = db.Column(db.Text    , nullable= True, default=None)

    #ForeginKey Columns:
    deal_id         = db.Column(db.Integer, db.ForeignKey('deal.id'))
    expenditure_id  = db.Column(db.Integer, db.ForeignKey('expenditure.id'))


class Notes(db.Model):
    __tablename__ = 'notes'

    #Attribute Columns:
    id        = db.Column(db.Integer   , primary_key=True)

    title     = db.Column(db.String(50), nullable= False, default= 'Title')
    content   = db.Column(db.Text      , nullable= True , default= None)
    date_time = db.Column(db.DateTime  , nullable= False)

    #ForeginKey Columns:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Expenditure(db.Model):
    __tablename__ = 'expenditure'

    #Attribute Columns:
    id   = db.Column(db.Integer,     primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    #Relationships:
    transactions = db.relationship("Transaction", backref="expenditure_object", lazy=True)

    @property
    def serialize(self):
        return {
            "id"   : self.id,
            "name" : self.name
        }


class File(db.Model):
    __tablename__ = 'file'

    #Attribute Columns:
    id     = db.Column(db.Integer                      , primary_key=True)
    format = db.Column(db.String(20)                   , nullable=False )
    data   = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)

    #ForeginKey Columns:
    deal_id  = db.Column(db.Integer, db.ForeignKey('deal.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))

    @property
    def serialize(self):
        '''
        Return object data in easily serializable format
        '''
        return {
            'id'       : self.id,               
            'format'   : self.format,
            'data'     : self.data,
            'deal_id'  : self.deal_id,
            'buyer_id' : self.buyer_id
        }
    
     
    


