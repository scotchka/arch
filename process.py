LOAD_WORD = 0x01
STORE_WORD = 0x02
ADD = 0x03
SUB = 0x04
ADD_ONE = 0x05  # second parameter unused
HALT = 0xFF


def from_twos(value, bits=16):
    assert 0 <= value < 2 ** bits
    if value < 2 ** bits / 2:
        return value
    else:
        return value - 2 ** bits


def to_twos(value, bits=16):
    assert -(2 ** bits) / 2 <= value < 2 ** bits / 2
    if value >= 0:
        return value
    else:
        return 2 ** bits + value


class Process:
    def __init__(self, memory):
        self.memory = memory
        self.registers = [0, 0, 0]

        print("input 1:", from_twos(self.memory[0x10] + 256 * self.memory[0x11]))
        print("input 2:", from_twos(self.memory[0x12] + 256 * self.memory[0x13]))

    def run(self):

        while True:
            pc = self.registers[0]
            instruction = self.memory[pc]
            if instruction == HALT:
                print("HALT")
                break
            elif instruction == LOAD_WORD:
                print("LOAD")
                r_idx = self.memory[pc + 1]
                in_idx = self.memory[pc + 2]
                self.registers[r_idx] = (
                    self.memory[in_idx] + 256 * self.memory[in_idx + 1]
                )
            elif instruction == STORE_WORD:
                print("STORE")
                r_idx = self.memory[pc + 1]
                in_idx = self.memory[pc + 2]
                value = self.registers[r_idx]
                self.memory[in_idx] = value % 256
                self.memory[in_idx + 1] = value // 256
            elif instruction == ADD:
                print("ADD")
                left = self.memory[pc + 1]
                right = self.memory[pc + 2]
                self.registers[left] = to_twos(
                    from_twos(self.registers[left]) + from_twos(self.registers[right])
                )
            elif instruction == SUB:
                print("SUB")
                left = self.memory[pc + 1]
                right = self.memory[pc + 2]
                self.registers[left] = to_twos(
                    from_twos(self.registers[left]) - from_twos(self.registers[right])
                )
            elif instruction == ADD_ONE:
                print("ADD ONE")
                left = self.memory[pc + 1]
                self.registers[left] = to_twos(from_twos(self.registers[left]) + 1)
            else:
                print("Should not get here.")
                return

            self.registers[0] += 3

            print(self.memory, self.registers)

        print("output", from_twos(self.memory[0x0E] + 256 * self.memory[0x0F]))


if __name__ == "__main__":
    memory = bytearray(
        [
            0x01,
            0x01,
            0x10,  # instructions
            0x01,
            0x02,
            0x12,
            0x04,
            0x01,
            0x02,
            0x02,
            0x01,
            0x0E,
            0xFF,
            0x00,  # reserved empty byte
            0x00,
            0x00,  # output
            0xF4,
            0xFF,  # input 1
            0x9C,
            0xFF,  # input 2
        ]
    )

    assert len(memory) == 20

    proc = Process(memory)

    proc.run()
