import discord
from discord.ext import commands
from settings import *


intents = discord.Intents(members=True, presences=True, guilds=True, messages=True, reactions=True)
afk1 = {}
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():  # Bot'un çalıştığını anlamamız için konsola bir yazı basar ve bot'un durumunu ayarlar.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=ReadyStatus))
    print('Access Granted.')


@bot.event
async def on_member_join(member):  # Sunucuya yeni birisi geldiğinde Hoş geldin mesajı atar ve Basic Role verir.
    channel1 = bot.get_channel(welcome)
    channel2 = bot.get_channel(welcomelog)
    role = member.guild.get_role(autorole)

    await channel1.send(f'Aramıza hoş geldin <@{member.id}>. İyi eğlencelerrr :tada:',
                        delete_after=5)
    await channel2.send(f'{member} kullanıcısı sunucuya katıldı.')
    await member.add_roles(role)


@bot.event
async def on_member_remove(member):  # Sunucudan birisi çıkış yaptığında log'a mesaj atar.
    channel = bot.get_channel(welcomelog)

    await channel.send(f'<@{member.id}> kullanıcısı aramızdan ayrıldı. :unamused:')


@bot.command()
async def avatar(ctx, *, user: discord.Member = None):  # Avatar yani profil fotoğrafı büyütme komutudur.

    author = ctx.author

    if not user:
        user = author

    if user.is_avatar_animated():
        url = user.avatar_url_as(format="gif")
    if not user.is_avatar_animated():
        url = user.avatar_url_as(static_format="png")

    await ctx.send("{}".format(url))


@bot.command()
async def clear(ctx, amount=7):  # Toplu mesaj silme komutudur.

    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f'``{amount} mesaj başarıyla silinmiştir.``',
                           delete_after=5)


@commands.has_permissions(kick_members=True)  # Sunucudan üye atma komutudur.
@bot.command()
async def kick(ctx, user: discord.Member, *, reason="**Belirtilmedi**"):
    channel = bot.get_channel(cezalog)
    kickk = discord.Embed(
        title=f"{user.name} kullanıcısı sunucudan başarıyla **atıldı**!",
        description=f"**Sebep**: **{reason}**\n **Eylemi Yapan**: **{ctx.author.mention}**").set_author(
        name="Kicked").set_thumbnail(
        url="https://cdn.discordapp.com/avatars/670012461537034255/9dea76961301911ce765151beb7b1c93.png?size=1024")
    await user.kick(reason=reason)
    await ctx.message.delete()
    await channel.send(embed=kickk)
    await ctx.channel.send(
        f'{user.mention} kullanıcısı sunucudan başarıyla **atıldı**. Eylemi yapan **yetkili** :  {ctx.author.mention}',
        delete_after=7)


@commands.has_permissions(ban_members=True)  # Sunucudan üye yasaklama komutudur.
@bot.command(aliases=["det"])
async def ban(ctx, user: discord.Member, *, reason="**Belirtilmedi**"):
    channel = bot.get_channel(cezalog)
    urll = user.avatar_url
    print(urll)
    bann = discord.Embed(title="",
                         description=f"**Sebep**: **{reason}**\n **Eylemi Yapan**: **{ctx.author.mention}**").set_thumbnail(
        url=f"{urll}").set_author(name = user.display_name, url = f"{user.default_avatar_url}")
    await user.ban(reason=reason)
    await ctx.message.delete()
    await channel.send(embed=bann)
    await ctx.channel.send(
        f'{user.mention} kullanıcısı sunucudan başarıyla **yasaklandı**. Eylemi yapan **yetkili** :  {ctx.author.mention}',
        delete_after=7)


@commands.has_permissions(ban_members=True)  # Sunucudan yasaklı üyelerin yasağını kaldırmak için kullanlıan komuttur.
@bot.command(pass_context=True)
async def unban(ctx, *, user=None):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Kullanıcı bulunamadı.")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason=f"Yasağı kaldıran yetkili:" + str(ctx.author))
            unbann = discord.Embed(
                title=f"{user.name} kullanıcısı yasaklaması başarıyla **kaldırıldı**!",
                description=f"**Eylemi Yapan**: **{ctx.author.mention}**").set_author(
                name="Unbann")
            await ctx.channel.send(embed=unbann,
                                   delete_after=5)
        else:
            await ctx.send("Kullanıcı yasaklı **değil**!")
            return

    except discord.Forbidden:
        await ctx.send("Kullanıcının yasağını kaldırmak için **yeterli yetkim** yok.")
        return

    except:
        await ctx.send("Yasaklama kaldırma __**başarılamadı**__.")
        return


@commands.has_permissions(manage_roles=True)  # Etiketlediğiniz kişiye rol verir.
@bot.command()
async def rolver(ctx, member: discord.Member, role: discord.Role):
    if role is None:
        await ctx.send('Lütfen bir rol etiketleyiniz.')

    else:

        await member.add_roles(role.id)


@commands.has_permissions(manage_roles=True)# Sunucuda belirlediğiniz bir rolü verir. Aliases bölümüne "" içinde yetkinizin adını yazarsanız (.yetkiismi) şeklinde kullanabilir
@bot.command(aliases=[])
async def rol1(ctx, member: discord.Member):
    yetkilirol1 = member.guild.get_role(yetki1)
    rolelog1 = bot.get_channel(rolelog)
    response = discord.Embed(
        description=f"**<@{member.id}> kullanıcısına <@&{yetkilirol1.id}> yetkisi verildi. \nYetkiyi veren**: **{ctx.author.mention}**")

    await ctx.channel.send(embed=response, delete_after=5)
    await rolelog1.send(
        f'Bir adet {yetkilirol1} yetkisi verildi. Yetki verilen: {member.mention}, Yetkiyi veren: {ctx.author.mention}')
    await member.add_roles(yetkilirol1)


@commands.has_permissions(manage_roles=True)
@bot.command(aliases=[])
async def rol2(ctx, member: discord.Member):
    yetkilirol2 = member.guild.get_role(yetki2)
    rolelog1 = bot.get_channel(rolelog)
    response = discord.Embed(
        description=f"**<@{member.id}> kullanıcısına <@&{yetkilirol2.id}> yetkisi verildi. \nYetkiyi veren**: **{ctx.author.mention}**")

    await ctx.channel.send(embed=response, delete_after=5)
    await rolelog1.send(
        f'Bir adet {yetkilirol2} yetkisi verildi. Yetki verilen: {member.mention}, Yetkiyi veren: {ctx.author.mention}')
    await member.add_roles(yetkilirol2)


@commands.has_permissions(manage_roles=True)
@bot.command(aliases=[])
async def rol3(ctx, member: discord.Member):
    yetkilirol3 = member.guild.get_role(yetki3)
    rolelog1 = bot.get_channel(rolelog)
    response = discord.Embed(
        description=f"**<@{member.id}> kullanıcısına <@&{yetkilirol3.id}> yetkisi verildi. \nYetkiyi veren**: **{ctx.author.mention}**")

    await ctx.channel.send(embed=response, delete_after=5)
    await rolelog1.send(
        f'Bir adet {yetkilirol3} yetkisi verildi. Yetki verilen: {member.mention}, Yetkiyi veren: {ctx.author.mention}')
    await member.add_roles(yetkilirol3)


@commands.has_permissions(manage_roles=True)
@bot.command(aliases=["dark"])
async def rol4(ctx, member: discord.Member):
    yetkilirol4 = member.guild.get_role(yetki4)
    rolelog1 = bot.get_channel(rolelog)
    response = discord.Embed(
        description=f"**<@{member.id}> kullanıcısına <@&{yetkilirol4.id}> yetkisi verildi. \nYetkiyi veren**: **{ctx.author.mention}**").set_author(name = member.display_name, url = f"{member.default_avatar_url}")

    await ctx.channel.send(embed=response, delete_after=5)
    await rolelog1.send(
        f'Bir adet {yetkilirol4} yetkisi verildi. Yetki verilen: {member.mention}, Yetkiyi veren: {ctx.author.mention}')
    await member.add_roles(yetkilirol4)


@commands.has_permissions(manage_guild=True) # Say komutu sunucunuz hakkında bilgi verir. Tagınız yok ise 197.satırı siliniz ve 210. satırdan Tag mesajının bulunduğu yeri siliniz.
@bot.command(pass_context=True)
async def say(ctx):
    count = 0
    tag = sum(tag1 in member.name for member in ctx.guild.members)
    uye = 0
    online = sum(member.status != discord.Status.offline for member in ctx.guild.members)

    for channel in ctx.guild.voice_channels:
        count = count + len(channel.members)
        continue

    users = tuple(ctx.guild.members)

    uye = uye + len(users)

    sayy = discord.Embed(title="",
                         description=f"Toplam seste ``{count}`` kişi bulunuyor.\n Toplam sunucuda ``{uye}``üye var.\n Toplam tagımızda ``{tag}`` kullanıcı bulunmakta.\n Toplam sunucuda aktif ``{online}`` üye var.")
    await ctx.channel.send(embed=sayy)



@bot.command() #Her yerde olan afk komutudur.
async def afk(ctx, *, reason = "Belirtilmedi!"):
    afk1[ctx.author.id] = reason
    if not "[AFK]" in ctx.author.display_name:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")


@bot.event 
async def on_message(message):
        
    try: 
        await bot.process_commands(message)

        if message.content.startswith(f"{prefix}afk1"):
            return

        if "[AFK]" in message.author.display_name:
            await message.author.edit(nick=message.author.display_name[6:])

        if message.author.id in afk1:
            afk1.pop(message.author.id)
            await message.channel.send("Başarıyla AFKdan çıktın!")

        mentions = sum(1 for user in message.mentions if afk1[user.id])

        if mentions == 0: 
            return

        if mentions > 1:
            await message.channel.send("Belirttiğin kullanıcılar şuanda AFK!")
            return
        else:
            reason = afk1[message.mentions[0].id]
            await message.channel.send(f"Belirttiğin kullanıcı şuanda {reason} sebebiyle AFK!")
    except:
        pass



bot.run(token)
