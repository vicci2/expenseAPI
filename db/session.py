# This file isused to bind the API to a database of choise and initiate a session upon connection or transaction:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Binding the database URI to that of the app:
# engine=create_engine("postgresql://qvgvkjifscbset:7f61ca772033504b2e03d05c8dd0eabec49a6841308091c5ede12f79be4d2c3e@ec2-63-34-180-86.eu-west-1.compute.amazonaws.com:5432/de8pm4atc92vpf")
engine=create_engine("postgresql://postgres:vicciSQL@localhost:5432/fast_expenses_api")
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)