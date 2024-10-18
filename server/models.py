# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    #Relationship mapping employee to related reviews
    reviews = db.relationship('Review', back_populates='employee', cascade='all, delete-orphan')

    # Relationship mapping employee to related onboarding
    onboarding = db.relationship(
        'Onboarding', uselist=False, back_populates='employee', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.hire_date}>"


class Onboarding(db.Model):
    __tablename__ = "onboardings"

    id = db.Column(db.Integer, primary_key=True)
    orientation = db.Column(db.DateTime)
    forms_complete = db.Column(db.Boolean, default=False)

    # Foreign key to store the employee id
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Relationship mapping onboarding to related employee
    employee = db.relationship('Employee', back_populates='onboarding')

    def __repr__(self):
        return f"<Onboarding {self.id}, {self.orientation}, {self.forms_complete}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    summary = db.Column(db.String)
    #Foreign key
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    #Relationship mapping the review to related employee
    employee = db.relationship('Employee', back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id}, {self.year}, {self.summary}>"







#error code I'm getting when initally trying to run 'flask db migrate -m "add foreign key to Review"
""" INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'reviews.employee_id'
INFO  [alembic.autogenerate.compare] Detected added foreign key (employee_id)(id) on table reviews
  Generating /Users/ianflurkey/Development/code/phase-4/python-p4-v2-one-many-
  relationships/server/migrations/versions/dabdcf797f35_add_foreign_key_to_review.py ...  done
(python-p4-v2-one-many-relationships) ianflurkey@Ians-MacBook-Air server % flask db upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 8fd6f63f0ac1 -> dabdcf797f35, add foreign key to Review
ERROR [flask_migrate] Error: No support for ALTER of constraints in SQLite dialect. Please refer to the batch mode feature which allows for SQLite migrations using a copy-and-move strategy. """

"""used following replacement code in alembic

def upgrade():
    # Commands to add a new column and foreign key to the existing table
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_reviews_employee_id_employees', 
            'employees', 
            ['employee_id'], 
            ['id']
        )

def downgrade():
    # Commands to remove the foreign key and column
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.drop_constraint('fk_reviews_employee_id_employees', type_='foreignkey')
        batch_op.drop_column('employee_id')
        
        """