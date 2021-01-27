def _pprint(mat):
    for row in mat:
        print(row)


def _placable(mat, point):
    if mat[point[0]][point[1]] == ' ':
        return True
    return False


def _check_rows(mat):
    for row in mat:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]

    return None


def _check_cols(mat):
    for j in range(3):
        if mat[0][j] == mat[1][j] == mat[2][j] and mat[0][j] != ' ':
            return mat[0][j]

    return None


def _check_diags(mat):
    if mat[0][0] == mat[1][1] == mat[2][2] and mat[0][0] != ' ':
        return mat[0][0]

    elif mat[0][2] == mat[1][1] == mat[2][0] and mat[1][1] != ' ':
        return mat[1][1]

    return None


def _check_state(mat):
    cr, cc, cd = _check_rows(mat), _check_cols(mat), _check_diags(mat)
    if cr:
        return cr

    elif cc:
        return cc

    return cd


def _change_player(player):
    if player == 'O':
        return'X'
    else:
        return 'O'


def _inside(point):
    return 0 <= point[0] <= 2 and 0 <= point[1] <= 2


def _no_move(mat):
    for row in mat:
        for col in row:
            if col == ' ':
                return False
    return True


def _valid_input(_input):
    try:
        _input = tuple(map(int, _input.split(',')))

    except:
        pass

    if isinstance(_input, tuple) or isinstance(_input, list):
        if isinstance(_input[0], int) and isinstance(_input[1], int):
            if _inside(_input):
                return _input
    return None


def play():
    mat = [[' ' for i in range(3)] for j in range(3)]
    player = 'O'
    _pprint(mat)
    while True:
        
        _input = None
        while not _input:
            _input = input('Enter a point: r,c \n')
            _input = _valid_input(_input)
        
        if _placable(mat, _input):
            mat[_input[0]][_input[1]] = player
            player = _change_player(player)
            
            _pprint(mat)
            game_over = _check_state(mat)
            if game_over:
                print('Winner is:', game_over)
                return

            if _no_move(mat):
                print('Draw!')
                return


if __name__ == '__main__':
    play()



















        


