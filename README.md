![Goldr logo](/imgs/goldr-logo.png)

# Goldr
A discord bot for eGLD holders, you can [invite Goldr](https://discord.com/api/oauth2/authorize?client_id=807967570962939914&permissions=10304&scope=bot) if you wish :) 

Enter your wallet ID and we will fetch data for your current eGLD balance, convert it in real time USD$ value.

## 100% Safe
- You'll have to retrieve your wallet ID as mentionned before and link it to the bot.
- There is not way for the bot to do anything malicious (sell / buy eGLD) with this information
- If you're uncomfortable linking your wallet in a discord channel, the bot offers you the possibility to be DM/PM-ed for linkage
- Bot respects RGPD/GDPR, you can remove your wallet only, change it, remove every information about you (even tho I only get your discord ID, discord Guild, discord Name and wallet)
- If the bot is present in more than 1 discord of yours and you don't want to share the same information from one discord to another, this is perfectly fine as we save your ID and the current server you're in. So if you are on server A and server B, and use the `egld$link` command on server A, server B won't be informed.

## Commands
### 👛 account related
- `egld$link` `<wallet_id>` Will link a wallet to yourself on the current discord
- `egld$unlink` Will unlink your wallet on the current discord

### 💸 money related
- `egld$wallet` Will display your current eGLD balance and convert it to USD$
- `egld$wallets` Will display everyone's eGLD balance and convert it to USD$ (only current discord, see above as to why)
- `egld$value` Will display current eGLD value in USD$. It can also retrieve any currency on binance for example `egld$value ETH_USDT` will get information on this page [ETH_USDT](https://www.binance.com/en-IN/trade/ETH_USDT) (see URL if you want to understand 😊)

### 📢 broad commands
- `me$set` `<wallet_id>` Will link a wallet to yourself to every discord the bot is in and you used previously. Example: If you are on server A and server B, both have the bot. You used a command in server A, but never in server B. If you DM / use `me$set`, it will set it only on A (server B doesn't know you exist since you never used any command in server B)
- `me$unset` Will unlink all wallet you linked to yourself
- `egld$help` Will display commands if you forgot them 😊

For more information see [help page](help).

## Thanks
- [Lycoon](https://github.com/Lycoon) for the assets he provided !
- Philippe for the idea !

## Deploying the bot yourself
You will need 3 files (don't put a newline in the files)
- `token` You will need to get a bot token from [dev discord](https://discord.com/developers/applications)
- `binance-key` For this two you will need to [create a Binance account](https://www.binance.com) and then [create an API KEY](https://www.binance.com/fr/my/settings/api-management)
- `binance-secret`
