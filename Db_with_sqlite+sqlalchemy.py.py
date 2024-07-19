from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user_client"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(Integer)
    endereco = Column(String)

    """Vinculo com a segunda tabela"""
    conta = relationship(
       "Conta", back_populates="user"
    )


    def __repr__(self):
      return f"""User(
          id={self.id},
          name={self.nome},
          cpf={self.cpf},
          endereco={self.endereco})"""


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    agencia = Column(Integer, nullable=False)
    numero = Column(String)
    saldo = Column(Float)

    """Gerando chave estrangeira realcionada com a primeira tabela"""
    user_id = Column(Integer, ForeignKey("user_client.id"))
    
    """vinculo"""
    user = relationship("User", back_populates="conta")


    def __repr__(self):
      return f"""Conta(
          id={self.id},
          tipo={self.tipo},
          num={self.numero},
          agencia={self.agencia}\n"""


#Gerando conexão com o banco

engine = create_engine("sqlite://",)
Base.metadata.create_all(engine)


#persistindo informações

with Session(engine) as session:
    eu = User(
       nome="maycon",
       cpf=12345678910,
       endereco="teste endereço",
       conta=[Conta(tipo='corrente',
                    agencia=1234567,
                    numero="1235748",
                    saldo=1000.0),
              Conta(tipo="poupança",
                     agencia=4563,
                     numero="00003",
                     saldo=50.0)]
       )
    
    joana = User(
       nome="joana",
       cpf=54782136925,
       endereco="segundo teste endereco",
       conta=[Conta(tipo='corrente',
                    agencia=321654,
                    numero="9987654",
                    saldo=500.0)]
    )

    session.add_all([eu, joana])

    session.commit()

#Apenas simples consultas

stmt = select(User).where(User.nome.in_(['joana']))

for user in session.scalars(stmt):
   print(user)

stmt_conta = select(Conta).where(Conta.user_id.in_([2]))

for user in session.scalars(stmt_conta):
   print(user)

#Apenas simples consultas

stmt = select(User).where(User.nome.in_(['maycon']))

for user in session.scalars(stmt):
   print(user)

stmt_conta = select(Conta).where(Conta.user_id.in_([1]))

for user in session.scalars(stmt_conta):
   print(user)