from models import Base, Session, User, Wallet, engine
import sqlalchemy


def commit(session):
    try:
        session.commit()
    # except sqlalchemy.exc.PendingRollbackError:
    #     print('user was registration')
    except sqlalchemy.exc.IntegrityError:
        print('user was registration')


def user_add(session, user):
    if user.id in [us.id for us in session.query(User).all()]:
        print('User in DB')
    else:
        session.add(user)
        print('User added')


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    session = Session()

    user_add(session, User(123, 'Alex', True))
    commit(session)
