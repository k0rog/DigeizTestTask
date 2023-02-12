from api.extensions import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    malls = db.relationship(
        'Mall',
        back_populates='account',
        cascade='all, delete',
        passive_deletes=True,
    )
