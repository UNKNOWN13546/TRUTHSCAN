import urllib.request

with urllib.request.urlopen('http://127.0.0.1:8000/TRUTHSCAN_STANDALONE.html') as resp:
    html = resp.read().decode('utf-8')
    assert 'id="view-landing" class="hidden' in html, 'view-landing is not hidden!'
    assert 'id="view-app" class="flex flex-col' in html, 'view-app is not visible!'
    assert "routeTo('/app', false);" in html, 'routeTo app is missing!'
    print('VERIFICATION SUCCESSFUL: TRUTHSCAN_STANDALONE.html opens directly into the app workspace!')
