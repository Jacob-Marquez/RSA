def main():
    # read public key (to get n)
    with open('public_key.txt') as f:
        n = int(f.readline().strip())
        _ = f.readline()  # discard e

    # read private key
    with open('private_key.txt') as f:
        n2 = int(f.readline().strip())
        d  = int(f.readline().strip())

    assert n == n2, "Public and private moduli differ!"

    # read ciphertext
    with open('ciphertext.txt') as f:
        c = int(f.read().strip())

    # decrypt
    m = pow(c, d, n)

    # write decrypted message
    with open('decrypted_message.txt', 'w') as f:
        f.write(str(m))

if __name__ == '__main__':
    main()