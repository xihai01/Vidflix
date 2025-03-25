from mongoengine import connect

def init_db():
    connect(host="mongodb+srv://xihailuo01:8EA4lGkoCmmz1zaR@vidflix-db.mpfnl.mongodb.net/?retryWrites=true&w=majority&appName=Vidflix-db")
    print('Connected to database: ')

# 91mM4C954FQ55LFw
# xihailuo01
# mongodb+srv://xihailuo01:8EA4lGkoCmmz1zaR@vidflix-db.mpfnl.mongodb.net/?retryWrites=true&w=majority&appName=Vidflix-db