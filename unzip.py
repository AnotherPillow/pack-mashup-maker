import os, re, zipfile, time

def unzip(path):
    appdata = os.getenv('APPDATA')

    if path != None:
        INPUT_DIR = path
    else:
        INPUT_DIR = os.path.join(appdata, '.minecraft', 'resourcepacks')

    def convert_chars(str):
        return re.sub(r'[^\x00-\x7F§]+', '_', str)

    if not os.path.exists('temp/'):
        os.makedirs('temp/')
    index = 0
    startTime = time.time()
    for root, dirs, files in os.walk(INPUT_DIR):
        index+=1
        for file in files:
            if file.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(root, file), 'r') as zip_ref:
                    try:
                        filename = file[:-4].split('     ')[1]
                    except IndexError:
                        filename = file[:-4]

                    filename = convert_chars(filename)
                    print(filename)
                    name = os.path.join('temp', file[:-4])
                    

                    
                    if not os.path.exists(name):
                        try:
                            zip_ref.extractall(name)
                        except:
                            print(f"Could not extract {filename}")
                            pass

    print(f"Unzipped packs in {time.time() - startTime} seconds")

if __name__ == '__main__':
    unzip()