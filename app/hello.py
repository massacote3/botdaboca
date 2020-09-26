# -*- coding:utf-8 -*-
import platform
import subprocess
from flask import Flask, Response, request
from tinydb import TinyDB, Query
from discord.ext import commands
from tabulate import tabulate
import threading
import discord
import random
import time
import sys
import os
KEY=os.getenv("SECRET_KEY")
app = Flask(__name__)
#=====================================><=============================#
#databse setup
drugs=TinyDB('drugs.json')
users=TinyDB('users.json')
switch=TinyDB('switch.json')
qr=Query()
#bot setup
client = discord.Client()
bot = commands.Bot(command_prefix='!')
#filing databases in case they're empty when the bot runs
names=['pó de 10', 'pó de 15','pino de 10','pino de 20','erva de 5','erva de 10','lança','bala']
prices={'pó de 10': 10, 'pó de 15': 15, 'pino de 10': 10, 'pino de 20': 20, 'erva de 5': 5, 'erva de 10': 10, 'lança': 10,'bala': 25}
bicos={'servente':50, 'mula':15, 'radinho':10, 'ajudante da dona neusa':0}

for name in names:
    ss=drugs.search(qr.name==name)
    if ss==[]:
        drugs.insert({'name':name,'price':prices.get(name)})
#=====================================><====================================#
async def on_ready():#login message
    print('We have logged in as {0.user}'.format(bot))
bot.add_listener(on_ready)
    
@bot.command()
async def comprar(ctx, drug, qtd):
    user=users.search(qr.name==ctx.author.name)[0]
    money=user['money']
    mention=ctx.author.mention
    inv=user['inventory']
    try:    
        prod=drugs.search(qr.name==drug)[0]
    except:
        await ctx.send('Coé menor nois num tem essa parada aqui não bota fé?')
    if prod:
        price=prod['price']
        if money>price:
            newmoney=money-price
            users.update({'money':newmoney}, qr.name==ctx.author.name)
            if prod['name'] not in inv.keys():
                inv[prod['name']]=1
                users.update({'inventory':inv}, qr.name==ctx.author.name)
                await ctx.send(f'{mention} comprou {qtd} {prod["name"]}')
            else:
                qt=inv.get(prod['name'])
                qt+=int(qtd)
                inv[prod['name']]=qt
                users.update({'inventory':inv}, qr.name==ctx.author.name)
                await ctx.send(f'{mention} comprou {qtd} {prod["name"]}')
        else:
            await ctx.send('Tá de caô comigo menor? essa merreca num compra nada aqui não')

@bot.command()
async def rinha(ctx, cock, bet):
    user=users.search(qr.name==ctx.author.name)[0]
    name=ctx.author.name
    mention=ctx.author.mention
    money=int(user['money'])
    cocks=['caramuru', 'indiano', 'carijó', 'geromel']
    if cock not in cocks:
        await ctx.send('Escolhe teu galo namoral parcero, sem caô comigo')
    else: 
        if money<int(bet):
            await ctx.send('Tá de tiração menor? junta a grana da aposta ae')
        else:
            choices=[1,0]
            nb=random.choice(choices)
            if nb==1:
                profit=int(bet)
                profit*=2
                money+=profit
                users.update({'money':money}, qr.name==ctx.author.name)
                current=users.search(qr.name==name)[0]['money']
                await ctx.send(f'{mention} Parábens cria, ganhou {profit} pila, tá patrão com {current} no bolso')
            else:
                money-=int(bet)
                users.update({'money':money}, qr.name==ctx.author.name)
                money=users.search(qr.name==name)[0]['money']
                current=users.search(qr.name==name)[0]['money']
                await ctx.send(f'{mention} Perdeu {bet} conto otário, só tem {current} no bolso, agora rala daqui')

@bot.command()
async def bico(ctx):
    name=ctx.author.name
    user=users.search(qr.name==ctx.author.name)[0]
    mention=ctx.author.mention
    money=int(user['money'])
    keys=[]
    for key in bicos.keys():
        keys.append(key)
    trampo=random.choice(keys)
    valor=bicos.get(trampo)
    money+=valor
    users.update({'money':money}, qr.name==ctx.author.name)
    await ctx.send(f'{mention} fez um bico de {trampo} e ganhou {valor} reais')   

@bot.command()
async def ranking(ctx):
    us=users.all()
    index=[]
    headers=['Usuário', 'Grana']
    tables=[]
    for i in us:
        index.append(i['money'])
    index.sort()
    inv=index[::-1]
    n=0
    for i in inv:
        user=users.search(qr.money==i)
        item=[]
        while n<len(us):
            try:    
                if [user[n]['name'],user[n]['money']] not in tables:
                    tables.append([user[n]['name'],user[n]['money']])
                    break
                else:
                    pass
                
            except:
                pass
            n+=1
    await ctx.send('Ranking da boca')
    await ctx.send('```'+tabulate(tables[:5], headers, tablefmt="psql")+'```')
    

@bot.command()
async def grana(ctx, qtd, *name):
    user=users.search(qr.name==ctx.author.name)[0]
    money=user['money']
    add=int(qtd)
    newmoney=money+add
    if ctx.author.name=='GERENTE DO PRETO':
        if not name:
            users.update({'money':newmoney}, qr.name==ctx.author.name)
            await ctx.send(f'Mais {qtd} pila pro patrão')
        else:
            users.update({'money':newmoney}, qr.name==name)
            await ctx.send(f'Mais {qtd} pila pro menor')
    else:
        print('debug4')
        pass
    
@bot.command()
async def inventario(ctx):
    name=ctx.author.name
    mention=ctx.author.mention
    inv=users.search(qr.name==name)[0]['inventory']
    headers=['Item', 'Quantidade']
    table=[]
    for key in inv.keys():
        item=[]
        item.append(str(key))
        item.append(str(inv.get(key)))
        table.append(item)
    await ctx.send(mention+'Seu inventário contém:')
    await ctx.send('```'+tabulate(table, headers, tablefmt="psql")+'```')
    
@bot.command()
async def carteira(ctx):
    name=ctx.author.name
    mention=ctx.author.mention
    money=users.search(qr.name==name)[0]['money']
    await ctx.send(f'{mention} você tem {money} reais')

@bot.command()
async def walker(ctx):
    await ctx.send('Walker vá a merda')

@bot.command()
async def caixadagua(ctx):
    await ctx.send('Ian, já resolveu a tela verde?')

@bot.command()
async def sulista(ctx):
    await ctx.send('ovo deletar o zapkkkkkkkk')

@bot.command()
async def poste(ctx):
    await ctx.send('Isaque acaba de cortar sua net')

@bot.command()
async def carioca(ctx):
    await ctx.send('carioca rico vai sortear uns games pra rapaziada')

@bot.command()
async def comandos(ctx):
    await ctx.send("""```Comandos do bot:
!comprar - compra a boa
produtos: pó de 10, pó de 15, pino de 10, pino de 20, erva de 5, erva de 10, lança e bala
usos: !comprar <produto> <quantidade>
=====================================================
!rinha - aposta no seu galo favorito 
galos: caramuru, indiano, carijó e geromel
usos: !rinha <nome do galo> <valor> 
=====================================================
!inventário - mostra seu inventário
=====================================================
!carteira - quanta grana tu tem
=====================================================
!bico - faz um bico pra ganhar uma merreca
=====================================================
!ranking - ranking da boca
====================================================
mais comandos quando o adm quiser, não sou empregado de ninguém```""")
    
#some debug commands
@bot.command()
async def usuarios(ctx):
    user=users.search(qr.name==ctx.author.name)[0]
    if ctx.author.name=='GERENTE DO PRETO':
        us=users.all()
        names=[]
        for i in us:
            names.append(i['name'])
        await ctx.send(names)
    else:
        pass
#======================><=======================#
@app.route('/')
def run():
    bot.run(KEY)
    time.sleep(10)
        value=switch.all()[0]['value']
        if value==1:
            switch.update({'value':0}, qr.value==1)
            pass
        else:
            switch.update({'value':1}, qr.value==0)
            sys.exit()
            
        us=[]
        for i in bot.users:
            if i.bot:
                pass
            else:
                us.append(i.name)
                ss=users.search(qr.name==i.name)
                if ss==[]:
                    users.insert({'name':i.name, 'xp':0, 'money':20, 'inventory':{}})
        
app.run()
