import os
import re
import requests

word_list_file = "five-letter-words.txt"

def read_word_list():
  if not os.path.exists(word_list_file):
    word_list_response = requests.get("https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears-medium.txt")
    content_as_string = word_list_response.content.decode("utf-8")
    lines = content_as_string.splitlines()
    words = [word for word in lines if len(word) == 5]
    
    with open(word_list_file, 'w') as f:
      for word in words:
          f.write(f"{word}\n")
  
  else:
    with open(word_list_file, 'r') as f:
      words = f.read().splitlines()

  return words

def get_word_dictionary(words):
  words_dict = dict()

  for word in words:
    key = "".join(sorted(word))
    if key not in words_dict:
      words_dict[key] = []

    words_dict[key].append(word)
  
  return words_dict  

def remove_words_with_double_letters(words):
  double_letters_regex = re.compile(r"(\w)\1+")
  filtered_words = { key:words for (key, words) in words.items() if not double_letters_regex.search(key)}
  return filtered_words

# From https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
letters_by_frequency = "eariotnslcudpmhgbfywkvxzjq"

def get_word_regex(source_letters, word_length, word_count):
  letters = source_letters[:(word_length * word_count)]
  letters = "".join(letters)
  regex = re.compile(f"[{letters}]{{{word_length}}}")
  return regex

def find_valid_words(letters, words, word_length, chosen_words, words_left):
  regex = get_word_regex(letters, word_length, words_left)
  candidates = [word for word in words if regex.match(word)]
  print(candidates)
  
  words_left = words_left - 1
  results = []
  partial_results = []
  for candidate in candidates:
    remaining_letters = [letter for letter in letters if letter not in candidate]
    remaining_words = [word for word in words if word != candidate]
    new_chosen_words = chosen_words + [candidate]
    if words_left == 0:
      results.append(new_chosen_words)
    else:
      partial_results.append((remaining_letters, remaining_words, word_length, new_chosen_words, words_left))

  if words_left == 0:
    return ("results", results)
  else:
    return ("partial_results", partial_results)
  
if __name__ == "__main__":
  word_list = read_word_list()
  words = get_word_dictionary(word_list)
  words = remove_words_with_double_letters(words)

  letters = [letter for letter in "abc"]
  words = ["abc", "def", "ghi"]
  word_length = 3
  chosen_words = []
  words_left = 1

  (type, result) = find_valid_words(letters, words, word_length, chosen_words, words_left)
  print(type)
  print(result)
