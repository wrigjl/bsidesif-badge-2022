import spectre

if __name__ == "__main__":
    print("Executed when ran directly")
    spectre.boot_init()
else:
   print("Executed when imported")