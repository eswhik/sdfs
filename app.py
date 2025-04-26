from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError

app = Flask(__name__)

@app.route('/get-iframe', methods=['GET'])
def get_iframe():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(target_url)
            page.wait_for_selector('iframe#embedIframe', timeout=5000)

            try:
                page.click('#cargar-canal', timeout=3000)
                page.wait_for_timeout(2000)
            except TimeoutError:
                pass

            iframe_src = page.locator('iframe#embedIframe').get_attribute('src')
            browser.close()

            if iframe_src:
                return jsonify({'iframe': iframe_src})
            else:
                return jsonify({'error': 'Iframe not found'}), 404

    except TimeoutError:
        return jsonify({'error': 'Timeout waiting for iframe or button'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
