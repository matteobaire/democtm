# coding=utf-8
MAX_LENGTH = 60
SPACES_ADDED = 25 * " "


class ScrollingText(object):
    def __init__(self, text, rotations=0):
        self.text = text
        self.rotations = rotations
        self.rotated_text = self.__rotate(self.text, self.rotations)

    def __str__(self):
        return self.rotated_text

    def __len__(self):
        return len(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __ne__(self, other):
        return self.text != other.text

    @staticmethod
    def __rotate(text, rotations):
        if rotations == 0:
            return text
        for rotation in xrange(rotations):
            text = text[1:] + text[0]
        return text

    def step_left(self):
        self.rotated_text = self.__rotate(self.rotated_text, 1)
        self.rotations += 1
        if self.rotations >= len(self.text):
            self.rotations = 0

    def step_right(self):
        self.rotated_text = self.rotated_text[-1] + self.rotated_text[0:-1]
        self.rotations -= 1
        if self.rotations < 0:
            self.rotations = 5

    def replace(self, other):
        if self == other:
            pass
        else:
            rotation = self.rotations
            self.text = other.text
            self.rotated_text = self.__rotate(self.text, rotation)


class MaskedText(object):
    def __init__(self, text):
        self.text = text
        self.mask = SPACES_ADDED
        self.masked_text = text
        self.apply_mask()

    def apply_mask(self):
        self.masked_text = "{}{}".format(self.mask, self.text)
        while len(self.masked_text) <= MAX_LENGTH:
            self.masked_text = ' ' + self.masked_text 

    def __str__(self):
        return self.masked_text

    def __len__(self):
        return len(self.masked_text)


if __name__ == '__main__':
    testo_1 = MaskedText("prova")
    testo_2 = MaskedText("Saratoga il silicone scintillante")
    print "{} {}".format(testo_1, len(testo_1))
    message = ScrollingText(str(testo_1), 0)
    another = ScrollingText(str(testo_2), 0)
    print "{} {}".format(message, len(message))
    for i in xrange(len(another) * 2):
        another.step_left()
        if another.rotations == 39:
            another.replace(message)
        print "{} {}".format(another, another.rotations)
    print "{} {}".format(another, another.rotations)
    print "{} {}".format(message, message.rotations)
