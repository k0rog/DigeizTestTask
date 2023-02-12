from api.extensions import db


class Mall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'))
    account = db.relationship('Account', back_populates='malls')

    units = db.relationship(
        'Unit',
        back_populates='mall',
        cascade='all, delete',
        passive_deletes=True,
    )
