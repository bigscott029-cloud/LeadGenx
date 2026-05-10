import logging
import os
from dotenv import load_dotenv
from main import LeadScrappingEngine
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError('TELEGRAM_BOT_TOKEN is required in environment or .env file')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

engine = LeadScrappingEngine('config.yaml')


def get_session_state(context: ContextTypes.DEFAULT_TYPE) -> dict:
    return context.user_data.setdefault('session', {
        'target_niche': None,
        'platforms': engine.config.get('bot', {}).get('default_platforms', ['web', 'linkedin', 'facebook', 'twitter', 'instagram']),
        'region': engine.config.get('bot', {}).get('default_region', ''),
        'amount': engine.config.get('bot', {}).get('default_amount', 50),
        'last_filepath': None,
    })


def build_help_text() -> str:
    return (
        'Lead Gen Bot Commands:\n'
        '/start - Initialize the bot session\n'
        '/help - Show this help message\n'
        '/status - Show current scraping settings\n'
        '/set_target <niche> - Choose a niche from config.yaml\n'
        '/set_platforms <platform1,platform2> - Choose platforms\n'
        '/set_region <region> - Apply a region filter for the next scrape\n'
        '/set_amount <number> - Set the maximum number of leads for the next scrape\n'
        '/scrape - Run scraping with current settings\n'
        '/download - Download the most recent results file'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    message = (
        'Welcome to the Lead Generation Bot!\n\n'
        'Use /help to see commands.\n'
        f"Current platforms: {', '.join(state['platforms'])}\n"
        f"Current region: {state['region'] or 'none'}\n"
        f"Max leads: {state['amount']}"
    )
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(build_help_text())


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    message = (
        'Current session settings:\n'
        f"Target niche: {state['target_niche'] or 'none'}\n"
        f"Platforms: {', '.join(state['platforms'])}\n"
        f"Region: {state['region'] or 'none'}\n"
        f"Maximum leads: {state['amount']}\n"
    )
    await update.message.reply_text(message)


async def set_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    args = context.args
    if not args:
        await update.message.reply_text('Usage: /set_target <niche>')
        return

    niche = ' '.join(args).strip()
    available = [n.get('name') for n in engine.config.get('niches', [])]
    if niche not in available:
        await update.message.reply_text(f"Niche not found. Available niches: {', '.join(available)}")
        return

    state['target_niche'] = niche
    await update.message.reply_text(f'Target niche set to: {niche}')


async def set_platforms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    args = context.args
    if not args:
        await update.message.reply_text('Usage: /set_platforms web,linkedin,facebook,twitter,instagram')
        return

    requested = [platform.strip().lower() for platform in ' '.join(args).split(',') if platform.strip()]
    available = [p.get('name') for p in engine.config.get('platforms', [])]
    valid = [platform for platform in requested if platform in available]

    if not valid:
        await update.message.reply_text(f"No valid platforms found. Available: {', '.join(available)}")
        return

    state['platforms'] = valid
    await update.message.reply_text(f"Platforms set to: {', '.join(valid)}")


async def set_region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    args = context.args
    if not args:
        await update.message.reply_text('Usage: /set_region <region>')
        return

    region = ' '.join(args).strip()
    state['region'] = region
    await update.message.reply_text(f'Region filter set to: {region}')


async def set_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    args = context.args
    if not args:
        await update.message.reply_text('Usage: /set_amount <number>')
        return

    try:
        amount = int(args[0])
        if amount <= 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text('Please provide a valid positive integer for lead count.')
        return

    state['amount'] = amount
    await update.message.reply_text(f'Maximum leads for next scrape set to: {amount}')


async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    await update.message.reply_text('Starting scraping job... this may take a few minutes.')

    leads = engine.run_scraping(
        platforms=state['platforms'],
        niche=state['target_niche'],
        regions=[state['region']] if state['region'] else [],
        max_leads=state['amount'],
    )

    if not leads:
        await update.message.reply_text('No leads were found. Try changing your niche, region, or platform selection.')
        return

    filepath = engine.save_leads()
    state['last_filepath'] = filepath
    await update.message.reply_text(f'Scrape complete. Collected {len(leads)} leads. Saved to {filepath}')


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_session_state(context)
    filepath = state.get('last_filepath')
    if not filepath or not os.path.exists(filepath):
        await update.message.reply_text('No results file available to download. Run /scrape first.')
        return

    await update.message.reply_document(document=open(filepath, 'rb'))


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('set_target', set_target))
    application.add_handler(CommandHandler('set_platforms', set_platforms))
    application.add_handler(CommandHandler('set_region', set_region))
    application.add_handler(CommandHandler('set_amount', set_amount))
    application.add_handler(CommandHandler('scrape', scrape))
    application.add_handler(CommandHandler('download', download))

    logger.info('Telegram bot started')
    application.run_polling()


if __name__ == '__main__':
    main()
