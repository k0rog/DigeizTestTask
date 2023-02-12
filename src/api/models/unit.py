from api.extensions import db


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id', ondelete='CASCADE'))
    mall = db.relationship('Mall', back_populates='units')
