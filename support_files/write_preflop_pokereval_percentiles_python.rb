require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'pp'

url = "http://www.caniwin.com/texasholdem/preflop/heads-up.php"
agent = Mechanize.new
page = agent.get(url)
rows = page.search("tr.pocRow0").to_a + page.search("tr.pocRow1").to_a

suited_result = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
unsuited_result = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

def convert_letter_rank_to_number(rank)
  if rank.downcase == "t"
    return 10
  elsif rank.downcase == "j"
    return 11
  elsif rank.downcase == "q"
    return 12
  elsif rank.downcase == "k"
    return 13
  elsif rank.downcase == "a"
    return 14
  else
    return rank.to_i
  end
end

for tr in rows
  cells = tr.search("td")
  hand_string = cells[1].content.strip
  # must use ruby 1.9.2 or it gets weird because this behavior has changed
  rank1 = convert_letter_rank_to_number(hand_string[0])
  rank2 = convert_letter_rank_to_number(hand_string[1])
  suited = hand_string[2] == "s"
  win_pct = cells[3].content.strip.to_f
  tie_pct = cells[4].content.strip.to_f
  total_pct = ((win_pct + tie_pct * 0.5) / 100).round(4)

  if suited
    suited_result[rank1][rank2] = total_pct
    suited_result[rank2][rank1] = total_pct
  else
    unsuited_result[rank1][rank2] = total_pct
    unsuited_result[rank2][rank1] = total_pct
  end
end

# now clean up the suited and unsuited results to fill with 0s
for i in (0..14)
  for j in (0..14)
    suited_result[i][j] = 0 if suited_result[i][j].nil?
    unsuited_result[i][j] = 0 if unsuited_result[i][j].nil?
  end
end

puts "suited_result = ["
for a in suited_result
  puts "#{a},"
end
puts "]"

puts "unsuited_result = ["
for a in unsuited_result
  puts "#{a},"
end
puts "]"