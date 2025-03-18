import click
from faker import Faker
from . import db

from .schema import User  # Adjust the import based on your project structure

@click.command('seed-db')
def seed_db_command():
  # Initialize Faker
  fake = Faker()

  # Seed the database with random users
  for _ in range(50):  # Generate 50 random users
    user = User(
      username=fake.user_name(),
      email=fake.email(),
      password=fake.password(),  # Ensure your User model hashes passwords if needed
    )
    user.save()

    click.echo("Database seeded with random users!")

def init_seed(app):
  app.cli.add_command(seed_db_command)