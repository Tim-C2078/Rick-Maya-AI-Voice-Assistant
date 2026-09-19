from playwright.sync_api import sync_playwright
from pathlib import Path
from time import sleep

PROFILE_DIR = Path("./edge_profile")


def helper_function_alert_window(page, text):
    def handle_dialog(dialog):
        sleep(5)
        dialog.accept()

    page.once("dialog", handle_dialog)
    page.evaluate("(text) => alert(text)", text)


def playwright_web_interaction_base(function, browser="msedge", *args):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel=browser,
            headless=False,
            slow_mo=1000,
            chromium_sandbox=True,
            ignore_default_args=["--enable-automation"],
            args=[
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-features=msEdgeAccountConsistency,EdgeWelcomePage",
                "--disable-sync",
            ],
            no_viewport=True,
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            if (!window.chrome) {
                window.chrome = {};
            }
            if (!window.chrome.runtime) {
                window.chrome.runtime = {};
            }

            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-GB', 'en']
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3]
            });
        """)

        context.set_default_timeout(120000)
        page = context.pages[0] if context.pages else context.new_page()

        for p in context.pages[1:]:
            p.close()

        function(context, page, *args)

        helper_function_alert_window(page, "Process Finished! Closing the window!")
        context.close()
