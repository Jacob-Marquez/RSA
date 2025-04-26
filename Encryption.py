def main():
    # read public key
    with open('public_key.txt') as f:
        n = int(f.readline().strip())
        e = int(f.readline().strip())

    # read message (an integer)
    with open('message.txt') as f:
        m = int(f.read().strip())

    # encrypt
    c = pow(m, e, n)

    # write ciphertext
    with open('ciphertext.txt', 'w') as f:
        f.write(str(c))

if __name__ == '__main__':
    main()