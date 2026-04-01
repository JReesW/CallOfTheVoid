pyinstaller --onedir --add-data "resources:resources" --distpath "./dist/Call of the Void.AppDir/usr" --clean -y --name "bin" --icon=resources/images/solo_avatar_transparent.png main.py
mv ./dist/Call\ of\ the\ Void.AppDir/usr/bin/bin ./dist/Call\ of\ the\ Void.AppDir/usr/bin/main
(cd dist && ./appimagetool-x86_64.AppImage ./Call\ of\ the\ Void.AppDir/)
