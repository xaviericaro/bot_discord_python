import discord
from discord.ext import commands, tasks
from datetime import time, datetime, timedelta
# Importando a biblioteca discord.py e comandos

intents = discord.Intents.all()
bot = commands.Bot('.', intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()  # Sincroniza os comandos do bot com o Discord
    print("------------------------------------------------------------------")
    print(f'Sincronizados {len(synced)} comandos.')
    print()
    enviar_mensagem_periodica.start()  # Inicia a tarefa periódica
    print("------------------------------------------------------")
    print(f'Bot {bot.user.name} está online!')
    print(f'ID do bot: {bot.user.id}')
    print(f'Prefixo do bot: {bot.command_prefix}')
    print()
    print(f'Bot inicializado com sucesso')
    print("------------------------------------------------------")

@bot.event
async def on_member_join(membro: discord.Member):
    canal = bot.get_channel(1378491880081195018) # ID do canal de boas-vindas
    await canal.send(f"{membro.mention} entrou no servidor! Seja bem-vindo(a)! :tada:")

@bot.event
async def on_member_remove(membro: discord.Member):
    canal = bot.get_channel(1378494858641281275) # ID do canal de despedidas
    await canal.send(f"{membro.mention} saiu do servidor! Sentiremos sua falta! :cry:")


@bot.command()
async def hey(ctx: commands.Context):
    nome = ctx.author.name
    print(f'Comando hey chamado por {nome}')
    await ctx.reply(f'Olá {nome}, como posso ajudar você hoje?')

@bot.command()
async def falar(ctx:commands.Context, *,texto):
    await ctx.msg.delete()
    await ctx.send(texto)

@bot.command()
async def somar(ctx:commands.Context, num1:int, num2:int):
    resultado = num1 + num2
    await ctx.reply(f'O resultado da soma entre {num1} e {num2} é: {resultado}')

@bot.command()
async def subtrair(ctx:commands.Context, num1:int, num2:int):
    if num1 < num2:
        await ctx.send("O primeiro número deve ser maior que o segundo para subtrair!")
        return
    resultado = num1 - num2
    await ctx.reply(f'O resultado da subtração entre {num1} e {num2} é: {resultado}')

@bot.command()
async def multiplicar(ctx:commands.Context, num1:int, num2:int):
    resultado = num1 * num2
    await ctx.reply(f'O resultado da multiplicação entre {num1} e {num2} é: {resultado}')

@bot.command()
async def dividir(ctx:commands.Context, num1:int, num2:int):
    if num2 == 0:
        await ctx.reply("Não é possível dividir por zero!")
    else:
        resultado = num1 / num2
        await ctx.reply(f'O resultado da divisão entre {num1} e {num2} é: {resultado}')

@bot.command()
async def tempo(ctx:commands.Context):
    agora = datetime.now()
    tempo_atual = agora.strftime("%H:%M:%S")
    data_atual = agora.strftime("%d/%m/%Y")
    await ctx.reply(f'Horario atual: {tempo_atual}\nData atual: {data_atual}')

@bot.command()
async def ping(ctx:commands.Context):
    tempo_ping = round(bot.latency * 1000)
    await ctx.reply(f'Pong! Latência: {tempo_ping}ms')

@bot.command()
async def avatar(ctx:commands.Context, membro:discord.Member=None):
    await ctx.msg.delete()
    if membro is None:
        membro = ctx.author
    avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
    embed = discord.Embed(title=f"Avatar de {membro.name}", color=discord.Color.blue())
    embed.set_image(url=avatar_url)
    embed.set_thumbnail(url=membro.default_avatar.url)
    embed.set_footer(text=f"ID do usuário: {membro.id}")
    await ctx.send(embed=embed)

@bot.command()
async def enviar_embed(ctx:commands.Context):
    await ctx.message.delete()  # Deleta a mensagem que chamou o comando
    # Cria uma embed personalizada
    minha_embed = discord.Embed()
    minha_embed.title = "Título da Embed"
    minha_embed.description = "Esta é uma descrição da embed."

    imagem = discord.File("imagens/bomdia.png",
    filename="bomdia.png")
    minha_embed.set_image(url="attachment://bomdia.png")
    minha_embed.set_thumbnail(url="attachment://bomdia.png")

    minha_embed.set_footer(text="Este é o rodapé da embed.")

    minha_embed.set_author(name="Goku", icon_url="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTsvdjXBRyYA542KN7utFtYgDqqoO1hKOUMjSjInup4o3bvBDsa3FgVaRhImDepifrPintjr0Yb3hKFPfob1y8GMT7ryX3a4rfZsAUs1w")

    await ctx.reply(embed=minha_embed, file=imagem)

@tasks.loop(hours=1)
async def enviar_mensagem_periodica():
    canal = bot.get_channel(1378430728647475210)
    if canal:
        hora_atual = datetime.now().strftime("%H:%M")
        mensagem = (f"Olá! A hora atual é {hora_atual}. Espero que você esteja tendo um ótimo dia!")
        await canal.send(mensagem)

@tasks.loop(minutes=30)
async def enviar_mensagem_30m():
    canal = bot.get_channel(1378430728647475210)
    await canal.send("Respeite as regras do servidor para manter a harmonia e evitar punições :smiley:")


@bot.tree.command()
async def hey(interaction: discord.Interaction):
    nome = interaction.user.name
    print(f'Comando hey chamado por {nome}')
    await interaction.response.send_message(f'Olá {nome}, como posso ajudar você hoje?',)

@bot.tree.command()
async def falar(interaction: discord.Interaction, texto: str):
    await interaction.response.send_message(texto,)

@bot.tree.command()
async def somar(interaction: discord.Interaction, num1: int, num2: int):
    resultado = num1 + num2
    await interaction.response.send_message(f'O resultado da soma entre {num1} e {num2} é: {resultado}')

@bot.tree.command()
async def subtrair(interaction: discord.Interaction, num1: int, num2: int):
    if num1 < num2:
        await interaction.response.send_message("O primeiro número deve ser maior que o segundo para subtrair!")
        return
    resultado = num1 - num2
    await interaction.response.send_message(f'O resultado da subtração entre {num1} e {num2} é: {resultado}')

@bot.tree.command()
async def multiplicar(interaction: discord.Interaction, num1: int, num2: int):
    resultado = num1 * num2
    await interaction.response.send_message(f'O resultado da multiplicação entre {num1} e {num2} é: {resultado}')

@bot.tree.command()
async def dividir(interaction: discord.Interaction, num1: int, num2: int):
    if num2 == 0:
        await interaction.response.send_message("Não é possível dividir por zero!", ephemeral=True)
    else:
        resultado = num1 / num2
        await interaction.response.send_message(f'O resultado da divisão entre {num1} e {num2} é: {resultado}')

@bot.tree.command()
async def tempo(interaction: discord.Interaction):
    agora = datetime.now()
    tempo_atual = agora.strftime("%H:%M:%S")
    data_atual = agora.strftime("%d/%m/%Y")
    await interaction.response.send_message(f'Horário atual: {tempo_atual}\nData atual: {data_atual}')

@bot.tree.command()
async def avatar(interaction: discord.Interaction, membro: discord.Member = None):
    if membro is None:
        membro = interaction.user
    avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
    embed = discord.Embed(title=f"Avatar de {membro.name}", color=discord.Color.blue())
    embed.set_image(url=avatar_url)
    embed.set_thumbnail(url=membro.default_avatar.url)
    embed.set_footer(text=f"ID do usuário: {membro.id}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def enviar_embed(interaction: discord.Interaction):
    await interaction.response.defer()
    # Cria uma embed personalizada
    minha_embed = discord.Embed()
    minha_embed.title = "Título da Embed"
    minha_embed.description = "Esta é uma descrição da embed."
    imagem = discord.File("imagens/bomdia.png", filename="bomdia.png")
    minha_embed.set_image(url="attachment://bomdia.png")
    minha_embed.set_thumbnail(url="attachment://bomdia.png")
    minha_embed.set_footer(text="Este é o rodapé da embed.")
    minha_embed.set_author(name="Goku", icon_url="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTsvdjXBRyYA542KN7utFtYgDqqoO1hKOUMjSjInup4o3bvBDsa3FgVaRhImDepifrPintjr0Yb3hKFPfob1y8GMT7ryX3a4rfZsAUs1w")
    await interaction.followup.send(embed=minha_embed, file=imagem)

@bot.tree.command()
async def ping(interaction: discord.Interaction):
    tempo_ping = round(bot.latency * 1000)
    await interaction.response.send_message(f'Pong! Latência: {tempo_ping}ms')


bot.run("MTM3ODQyNTg1MDk5NDc1MzUzNg.GDTz8-.TiMZzJ9E_eQBPjoM01fxh4sIzbv450AMngzeEg")