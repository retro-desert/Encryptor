# twofish implimentation
import math


# multiply 2 2d matricies together
# I could'nt be buggered adding exceptions so
# make sure your matricies are valid if for some
# insane reason you decide to take the code for the
# GF field matrix multiplications

# This is the second encryption code I wrote.Better than blowfish but
# still not great. I can't remember if I fixed the problems with special
# characters in the cypher text in here. There may also be problems with
# spliting stuff into blocks. Buyer beware.


# example use of the function for matrix multiplication
# in my notation a matrix is a list of lists. Each secondary list
# is a row

# This is written for python 3

##########################
## Mathmatics functions ##
##########################


# Multiplication in the GF(256) field
def GF256multiply(A, B):
    # multiply two numbers in the GF(256) field defined by field
    # This works using the peasents multiplication
    p = 0
    # V is the primitve polynomial
    V = 283
    # count through n
    for counter in range(8):
        if (B & 1) == 1:
            # add A to the product if B is odd like you
            # do in the peasents algorithm
            # does'nt hit when B has hit zero
            # to increase speed tell the code to stop
            # when B = 0
            p ^= A

        # shift A left
        A = A << 1

        # if A is outside the field use V to put it
        # back in
        if A >= 256:
            A = A ^ V
        # shift B one to the left
        B = B >> 1

    return p


# Matrix multiplication in the GF(256) field
def GF256matrixmultiply(A, B):
    C = []

    for i in range(len(A)):

        C.append([])

        for l in range(len(B[0])):

            a = 0

            for j in range(len(A[i])):
                a = a ^ (GF256multiply(A[i][j], B[j][l]))

            C[i].append(a)

    return C


# Plain old matrix multiplication
def matrixmultiply(A, B):
    C = []

    for i in range(len(A)):

        C.append([])

        for l in range(len(B[0])):

            a = 0

            for j in range(len(A[i])):
                a = a + (A[i][j] * B[j][l])

            C[i].append(a)

    return C


# find the transpose of a 2D marix
# I could'nt be buggered adding exceptions so
# make sure your matricies are valid
def transpose_matrix(A):
    T = []
    for i, element in enumerate(A[0]):

        T.append([])
        for l, line in enumerate(A):
            T[i].append(line[i])

    return T


# convert a list of values into the vector/matrix format
def transpose_vector(A):
    T = []
    for i, M in enumerate(A):
        T.append([int(M, 2)])

    return T


# bitwise rotation of a number rotdist bits to
# the left inside the field defined by bit_length
def ROL(number, rotdist, bit_length):
    # make it a 4 bit binary number
    a = pad_number(number, bit_length)
    # a

    # loop over the number of rotations needed
    for i in range(rotdist):

        # perform one rotation at a time
        b = ''
        # do the loop first. If it were not
        # for the looping we could use pythons
        # internal bitwise shift tools

        # move all the other elements in the string
        for l in range(bit_length - 1):
            b = b + a[l + 1]

        b = b + a[0]
        # alter a to ensure perminance over
        # all the shifts in the code
        a = b

    # print a
    return int(a, 2)


# bitwise rotation of a number rotdist bits to
# the right inside the field defined by bit_length
def ROR(number, rotdist, bit_length):
    # make it a 4 bit binary number
    a = pad_number(number, bit_length)
    # print a

    # loop over the number of rotations needed
    for i in range(rotdist):

        # perform one rotation at a time
        b = ''
        # do the loop first. If it were not
        # for the looping we could use pythons
        # internal bitwise shift tools
        b = b + a[bit_length - 1]
        # move all the other elements in the string
        for l in range(bit_length - 1):
            b = b + a[l]

        # alter a to ensure perminance over
        # all the shifts in the code
        a = b

    # print a
    return int(a, 2)


# perform the pseudo-hamilton transform
def PHT(a, b):
    a = int(a, 2)
    b = int(b, 2)

    A = (a + b) % pow(2, 32)
    B = (a + (2 * b)) % pow(2, 32)

    return [A, B]


################################################################################################
##### These are boring utilitarian functions that can be applied to any encryption program #####
################################################################################################


# convert a string representing the password
# to a long intiger
def pwdtokey(password):
    numbers = []

    for letter in password:
        numbers.append(ord(letter))

    pwdsum = 1
    for i in numbers:
        pwdsum *= i

    return pwdsum


# turn a number back into text
def num2text(number):
    binnumberlist = pad_number(number, 8)
    text = ''

    for i, binnumber in enumerate(binnumberlist):
        number = int(binnumber, 2)
        letter = chr(number)
        text = text + letter

    return text


# convert text to a number
def text2num(text):
    result = ''

    for lett in text:
        number = ord(lett)

        result = result + pad_number(number, 8)

    return int(result, 2)


# pad a number to a set number of bits and convert to binary
def pad_number(number, pad_val):
    # if the input number is less that 32 bits
    # the code returns a 32 bit binary string
    # if the number is more than 32 bits it
    # returns a list of 32 bit intergers
    number = bin(number)[2:]
    startlen = len(number)

    if startlen < pad_val:

        padinglen = pad_val - startlen

        padstring = '0' * padinglen

        number = padstring + number

    elif startlen > pad_val:

        units = int(startlen / pad_val)
        # set up the padding for the left over
        # non-64 bit integer
        extrabit = pad_val - (startlen % pad_val)

        pading = '0' * extrabit

        binnumber = pading + number

        number = []
        for i in range(units + 1):
            number.append(binnumber[0:pad_val])
            binnumber = binnumber[pad_val:]

    return number


# The H function takes a 32 bit word and a list of 32 bit words
# and produces a single 32 bit word. The number of rounds
# depends on the length of the list. There are 2=>4 q box/L XOR steps
# where the word is split into 4 8 bit words which are each passed
# through q0 or q1 boxes depending on the round. The words are then
# combined back into a 32 bit word and XORed with an element of L.
# The final step is a final set of q0/q1 boxes and then the resulting
# 8 bit words are converted into a vector and matrix multiplied with
# the MDS matrix in the GF(2^8) field
def H_function(W, L, MDS):
    # if there are four words in L do the first round of h
    # with L3. Round 1
    if len(L) > 3:
        w1 = int(W[0:8], 2)
        w2 = int(W[8:16], 2)
        w3 = int(W[16:24], 2)
        w4 = int(W[24:32], 2)

        w1 = q1(w1)
        w2 = q0(w2)
        w3 = q0(w3)
        w4 = q1(w4)

        w1 = pad_number(w1, 8)
        w2 = pad_number(w2, 8)
        w3 = pad_number(w3, 8)
        w4 = pad_number(w4, 8)

        W = w1 + w2 + w3 + w4

        W = int(W, 2) ^ int(L[3], 2)

        W = pad_number(W, 32)

        # if there are three or more words in L do the first round of h
    # with L2. Round 2
    if len(L) > 2:
        w1 = int(W[0:8], 2)
        w2 = int(W[8:16], 2)
        w3 = int(W[16:24], 2)
        w4 = int(W[24:32], 2)

        w1 = q0(w1)
        w2 = q0(w2)
        w3 = q1(w3)
        w4 = q1(w4)

        w1 = pad_number(w1, 8)
        w2 = pad_number(w2, 8)
        w3 = pad_number(w3, 8)
        w4 = pad_number(w4, 8)

        W = w1 + w2 + w3 + w4

        W = int(W, 2) ^ int(L[2], 2)

        W = pad_number(W, 32)

        # There must be at least 2 elements in L since the minimum
    # key length is 128 bits.Round 3

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    W = w1 + w2 + w3 + w4

    W = int(W, 2) ^ int(L[1], 2)

    W = pad_number(W, 32)
    # last round with a XOR step. XOR with L0

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    W = w1 + w2 + w3 + w4

    W = int(W, 2) ^ int(L[0], 2)

    W = pad_number(W, 32)
    # final round of q-boxes before the matrix multipliation

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    # now we need to multiply by the MDS matrix so we convert to
    # a vector using our established notation
    Word_vector = [[int(w1, 2)], [int(w2, 2)], [int(w3, 2)], [int(w4, 2)]]

    # do the multiplication remembering to stay in the 256 field
    # C is our result
    C = GF256matrixmultiply(MDS, Word_vector)

    # convert C into a 32 bit word by running throgh C and converting
    # the vector elements into binary and then combining the 8 bit words
    # into a 32 bit word
    Z = ''

    for i, c in enumerate(C):
        Z = Z + pad_number(c[0], 8)

    return Z


# function for the q1 s-box. Splits the number into two nibbles
# and then passes each of those nibbles through 3 mixing steps
# recombing them in the end the other way around
def q0(number):
    # not sure this is correct the twofish paper
    # was very sittily worded

    t = [[8, 1, 7, 13, 6, 15, 3, 2, 0, 11, 5, 9, 14, 12, 10, 4],
         [14, 12, 11, 8, 1, 2, 3, 5, 15, 4, 10, 6, 7, 0, 9, 13],
         [11, 10, 5, 14, 6, 13, 9, 0, 12, 8, 15, 3, 2, 4, 7, 1],
         [13, 7, 15, 4, 1, 2, 6, 14, 9, 11, 3, 0, 8, 5, 12, 10]]

    X = number

    # split the input into two nibbles
    a0 = int(X / 16)
    b0 = int(X % 16)

    # XOR nibble a0 and nibble b0 to get a1

    a1 = a0 ^ b0

    b1 = ((a0 ^ ROR(b0, 1, 4)) ^ (8 * a0)) % 16

    # move a1 and b1 through a substitution box
    [a2, b2] = [t[0][a1], t[1][b1]]

    # XOR nibble a2 and nibble b2 to get a3
    a3 = a2 ^ b2
    b3 = ((a2 ^ ROR(b2, 1, 4)) ^ (8 * a2)) % 16

    # move a3 and b3 through a substitution box
    [a4, b4] = [t[2][a1], t[3][b1]]

    # recombine the nibbles into a byte
    y = (16 * b4) + a4

    return y


# function for the q1 s-box. The same as the q0 s-box
# but with a different t vector
def q1(number):
    # not sure this is correct the twofish paper
    # was very sittily worded

    t = [[2, 8, 11, 13, 15, 7, 6, 14, 3, 1, 9, 4, 0, 10, 12, 5],
         [1, 14, 2, 11, 4, 12, 3, 7, 6, 13, 10, 5, 15, 9, 0, 8],
         [4, 12, 7, 5, 1, 6, 9, 10, 0, 14, 13, 8, 2, 11, 3, 15],
         [11, 9, 5, 1, 12, 3, 13, 14, 6, 4, 7, 15, 2, 0, 8, 10]]

    X = number

    # split the input into two nibbles
    a0 = int(X / 16)
    b0 = int(X % 16)

    # XOR nibble a0 and nibble b0 to get a1

    a1 = a0 ^ b0
    b1 = ((a0 ^ ROR(b0, 1, 4)) ^ (8 * a0)) % 16

    # move a1 and b1 through a substitution box
    [a2, b2] = [t[0][a1], t[1][b1]]

    # XOR nibble a2 and nibble b2 to get a3
    a3 = a2 ^ b2
    b3 = ((a2 ^ ROR(b2, 1, 4)) ^ (8 * a2)) % 16

    # move a3 and b3 through a substitution box
    [a4, b4] = [t[2][a1], t[3][b1]]

    # recombine nibbles into a byte
    y = (16 * b4) + a4

    return y


def find_M_vectors(Key):
    # find the binary key to see what we should pad to
    bin_key = bin(Key)
    bin_key = bin_key[2:]

    # work out what length to make the key. There are 3 break points
    # at 128, 192 and 256 bits. If were under a break point we pad out to
    # the next one
    if len(bin_key) <= 128:
        N = 128
    elif len(bin_key) > 128 or len(Key) <= 192:
        N = 192
    elif len(bin_key) <= 256:
        N = 256

    # Pad the key to N bits
    Key = pad_number(Key, N)

    N = len(Key)
    # find lower case k
    k = N / 64

    # find the vector denoted by a lowercase m
    # in the paper
    mk = []
    mij = ''
    for i, digit in enumerate(Key):

        mij = mij + digit

        if len(mij) == 8:
            mk.append(mij)
            mij = ''

    Mi = []
    mi = ''
    # split the key into words for the vector Mi
    for i, word in enumerate(mk):

        mi = mi + word
        if len(mi) == 32:
            Mi.append(mi)
            mi = ''

    # sort the words into Mo and Me
    Mo = []
    Me = []
    for i, m in enumerate(Mi):

        if (1 + i) % 2 == 1:
            Me.append(m)
        else:
            Mo.append(m)

    return [mk, Mo, Me, Mi]


def generate_K(Me, Mo, rounds=16):
    # The MDS matrix
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    rho = pow(2, 24) + pow(2, 16) + pow(2, 8) + pow(2, 0)

    # rint rho

    A = []
    B = []
    K = []
    for i in range(rounds + 8):
        a = pad_number((2 * i * rho), 32)
        A = int(H_function(a, Me, MDS), 2)
        b = pad_number(((2 * i) + 2) * rho, 32)
        B = ROL(int(H_function(b, Mo, MDS), 2), 8, 32)
        K.append((A + B) % pow(2, 32))
        K.append(ROL(((A + (2 * B)) % pow(2, 32)), 9, 32))

    return K


def find_S_vector(mk):
    # The RS matrix
    RS = [[1, 164, 85, 135, 90, 88, 219, 158],
          [164, 86, 130, 243, 30, 198, 104, 229],
          [2, 161, 252, 193, 71, 174, 61, 25],
          [164, 85, 135, 90, 88, 219, 158, 3]]

    # convert mk so it can be used by our
    # matrix multiplication functions
    T = transpose_vector(mk)

    S_vector = [[], [], [], []]
    # rint T
    k = len(mk) / 8

    for i in range(int(len(mk) / 8)):

        V = T[(8 * i): (8 * i) + 8]

        # multiply the RS matrix by V in the GF(2^8) field
        si = GF256matrixmultiply(RS, V)

        for l, s in enumerate(si):
            S_vector[l].append(s)

    S = []
    for i in range(len(S_vector[0])):

        # S.append('')
        Si = ''
        for l in range(len(S_vector)):
            Si = Si + pad_number(S_vector[l][i][0], 8)

        S.append(Si)

    return S


def gen_keys(key, N=128, rounds=16):
    key_lengths = [128, 192, 256]

    m = pwdtokey(key)

    # if the password is too long cut it down to fit
    if len(bin(m)[2:]) > N:
        m = int(bin(m)[2:N + 2], 2)

    [mk, Mo, Me, Mi] = find_M_vectors(m)

    # find the s-boxes
    bin_key = bin(m)
    bin_key = bin_key[2:]
    paded_key = pad_number(m, 128)

    S = find_S_vector(mk)

    K = generate_K(Me, Mo, rounds)

    return [K, S]


############################################################################
## These are the functions that actually do the encryption and decryption ##
############################################################################


def encrypt_word(message, S, K, rounds=16):
    # The MDS matrix
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    m = message
    # E is the message in the process of encryption
    # split the message into 4 32 bit words
    E = []
    for i in range(4):
        E.append(m[(i * 32):((i * 32) + 32)])

    # First do the whitening
    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i], 32)

    # convert the elements of E to intigers
    e = []
    for i, ee in enumerate(E):
        e.append(int(E[i], 2))

    # the fistal network runs 'rounds' times
    for r in range(rounds):
        # now enter the fistel network
        # create a vector for temporary values
        e = [[], [], [], []]

        # first find the things to XOR with E[2] and E[3]
        # E[2] and E[3] are the only things that change during F
        e[0] = H_function(E[0], S, MDS)

        e[1] = ROL(int(E[1], 2), 8, 32)
        e[1] = pad_number(e[1], 32)
        e[1] = H_function(e[1], S, MDS)

        [e[0], e[1]] = PHT(e[0], e[1])

        e[0] = (e[0] + K[(2 * r) + 8]) % pow(2, 32)
        e[1] = (e[1] + K[(2 * r) + 9]) % pow(2, 32)

        e[2] = e[0] ^ int(E[2], 2)
        e[2] = ROR(e[2], 1, 32)

        e[3] = ROL(int(E[3], 2), 1, 32)
        e[3] = e[3] ^ e[1]

        # swap the position of the 32 bit words
        E = [pad_number(e[2], 32), pad_number(e[3], 32), E[0], E[1]]

    # whiten the 32 bit words again
    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i + 4], 32)

    # print E
    # recombine the 32 bit words

    C = E[0] + E[1] + E[2] + E[3]

    return C


def decrypt_word(Cyphertext, S, K, rounds=16):
    # The MDS matrix
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    C = Cyphertext
    # print C
    # E is the message in the process of encryption
    # split the message into 4 32 bit words
    E = []
    for i in range(4):
        E.append(C[(i * 32):((i * 32) + 32)])

    # rint E

    # whiten the cyphertext
    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i + 4], 32)

    # the fistal network runs 'rounds' times
    for R in range(rounds):
        # we have to reverse the process so r = Rounds - r
        r = rounds - 1 - R
        # swap the position of the 32 bit words

        E = [E[2], E[3], E[0], E[1]]

        # now enter the fistel network
        # create a vector for temporary values
        e = [[], [], [], []]

        # first find the things to XOR with E[2] and E[3]
        # E[2] and E[3] are the only things that change during F
        e[0] = H_function(E[0], S, MDS)

        e[1] = ROL(int(E[1], 2), 8, 32)
        e[1] = pad_number(e[1], 32)
        e[1] = H_function(e[1], S, MDS)

        [e[0], e[1]] = PHT(e[0], e[1])

        e[0] = (e[0] + K[(2 * r) + 8]) % pow(2, 32)
        e[1] = (e[1] + K[(2 * r) + 9]) % pow(2, 32)

        # do the changing of E[2]/E[3] in reverse

        e[2] = ROL(int(E[2], 2), 1, 32)
        e[2] = e[0] ^ e[2]

        e[3] = int(E[3], 2) ^ e[1]
        e[3] = ROR(e[3], 1, 32)

        for i, ee in enumerate(e):
            e[i] = pad_number(ee, 32)

        E = [E[0], E[1], e[2], e[3]]

    # remove the first whitening step
    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i], 32)

    p = E[0] + E[1] + E[2] + E[3]

    # P = int(p, 2)

    # P = num2text(P)
    # return the encrypted message
    return p


def encrypt_message(message, S, K, rounds=16):
    # print(len(message) % 16)
    # convert the message to numbers to prevent character bugs
    message_num = text2num(message)

    # print(message_num)

    to_encrypt = pad_number(message_num, 128)
    # print(to_encrypt)

    # if the target is shorter than 128 bits make sure its still a list
    if not isinstance(to_encrypt, list):
        to_encrypt = [to_encrypt]

    cypher_text = ''
    for i, word in enumerate(to_encrypt):
        cypher_word = encrypt_word(word, S, K, rounds)

        cypher_text = cypher_text + cypher_word

    C = int(cypher_text, 2)

    number_C = C

    C = num2text(C)

    return [number_C, C]


def decrypt_message(message, S, K, rounds=16):
    # message_num = text2num(message)

    to_encrypt = pad_number(message, 128)

    # if the target is shorter than 128 bits make sure its still a list
    if not isinstance(to_encrypt, list):
        to_encrypt = [to_encrypt]

    cypher_text = ''
    for i, word in enumerate(to_encrypt):
        cypher_word = decrypt_word(word, S, K, rounds)

        cypher_text = cypher_text + cypher_word

    C = int(cypher_text, 2)

    C = num2text(C)

    return C


######################
## End of functions ##
######################


# set the key
key = 'VkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!'
N = 128
rounds = 16


def start():
    global K, S
    [K, S] = gen_keys(key, N, rounds)


# start()

# there's a wierd bug where if the number of characters is a certan amount a random
# set of characters appear at the beginning. It's really strange

test = 'Lol)'


def encrypt():
    global Cypher_text, num_C
    [num_C, Cypher_text] = encrypt_message(test, S, K)


# encrypt()

# print(Cypher_text)

def decrypt():
    global plain_text
    message_num = text2num(test)
    plain_text = decrypt_message(message_num, S, K, rounds=16)
# decrypt()

# print(plain_text)
