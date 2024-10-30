def convertingToCharacters(predicted_labels, num):
    
    chars = predicted_labels
    charsnum = num

    classes = {
        "0": " ",
        "1": "അ",
        "2": "ആ",
        "3": "ഇ",
        "4": "ഉ",
        "5": "ഋ",
        "6": "എ",
        "7": "ഏ",
        "8": "ഒ",
        "9": "ക",
        "10": "ഖ",
        "11": "ഗ",
        "12": 'ഘ',
        "13": "ങ",
        "14":  "ച",
        "15": "ഛ",
        "16": 'ജ',
        "17": "ഝ",
        "18": "ഞ",
        "19": "ട",
        "20": "ഠ",
        "21": "ഡ",
        "22": "ഢ",
        "23": "ണ",
        "24": "ത",
        "25": "ഥ",
        "26": "ദ",
        "27": "ധ",
        "28": "ന",
        "29": "പ",
        "30": "ഫ",
        "31": "ബ",
        "32": "ഭ",
        "33": "മ",
        "34": "യ",
        "35": "ര",
        "36": "റ",
        "37": "ല",
        "38": "ള",
        "39": "ഴ",
        "40": "വ",
        "41": "ശ",
        "42": "ഷ",
        "43": "സ",
        "44": "ഹ",
        "45": "ൺ",
        "46": "ൻ",
        "47": "ർ",
        "48": "ൽ",
        "49": "ൾ",
        "50": "ക്ക",
        "51": "ക്ഷ",
        "52": "ങ്ക",
        "53": "ങ്ങ",
        "54": "ച്ച",
        "55": "ഞ്ച",
        "56": "ഞ്ഞ",
        "57": "ട്ട",
        "58": "ണ്ട",
        "59": "ണ്ണ",
        "60": "ത്ത",
        "61": "ദ്ധ",
        "62": "ന്ത",
        "63": "ന്ദ",
        "64": "ന്ന",
        "65": "പ്പ",
        "66": "മ്പ",
        "67": "മ്മ",
        "68": "യ്യ",
        "69": "ല്ല",
        "70": "ള്ള",
        "71": "വ്വ",
        "72": "ാ",
        "73": "ി",
        "74": "ീ",
        "75": "ു",
        "76": "ൂ",
        "77": "ൃ",
        "78": "െ",
        "79": "േ",
        "80": "ൗ",
        "81": "ം",
        "82": "്യ",
        "83": "്ര",
        "84": "്വ",
}

    characters = [classes[str(c)] for c in chars]

    print(characters)

    new_list = []

    # Index for tracking the current position in the 'lines' list
    lines_index = 0

    for c in characters:
        new_list.append(c)
        charsnum[lines_index] -= 1  # Decrease the count for the current line

        if charsnum[lines_index] == 0:  # Check if the count for the current line has reached 0
            new_list.append('\n')  # Add newline character
            lines_index += 1  # Move to the next line count from the 'lines' list
            if lines_index >= len(charsnum):  # Check if all line counts have been processed
                break

    new_list = [str(item) for item in new_list]

    char_string = ','.join([str(item) for item in new_list])

    symbol_to_remove = ","

    new_string = ""
    for char in char_string:
        if char != symbol_to_remove:
            new_string += char

    return new_string