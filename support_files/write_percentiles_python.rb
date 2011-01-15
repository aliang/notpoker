fh = File.open("7462.txt","r")
# first just collect the stats
ec_size_5 = []
ec_size_6 = []
ec_size_7 = []
while line = fh.gets
  fields = line.split(" ")
  ec_size_5 << fields[1].to_i
  ec_size_6 << fields[2].to_i
  ec_size_7 << fields[3].to_i
end
fh.close

total_5_hands = ec_size_5.inject(:+)
total_6_hands = ec_size_6.inject(:+)
total_7_hands = ec_size_7.inject(:+)

percentile_5 = []
percentile_6 = []
percentile_7 = []
(1..7461).map { |rank|
  # you beat hands lower than your rank
  hands_beaten_5 = ec_size_5[rank..-1].inject(:+)
  hands_beaten_6 = ec_size_6[rank..-1].inject(:+)
  hands_beaten_7 = ec_size_7[rank..-1].inject(:+)
  percentile_5 << hands_beaten_5.to_f / total_5_hands
  percentile_6 << hands_beaten_6.to_f / total_6_hands
  percentile_7 << hands_beaten_7.to_f / total_7_hands
}
# don't forget 7462
percentile_5 << 0
percentile_6 << 0
percentile_7 << 0

fh = File.open("percentiles_5.py", "w")
fh.puts("percentiles_5_cards = [")
(0..7461).each do |i|
  fh.print "\n" if i % 4 == 0
  fh.print "#{percentile_5[i]},"
end
fh.puts("]")

fh = File.open("percentiles_6.py", "w")
fh.puts("percentiles_6_cards = [")
(0..7461).each do |i|
  fh.print "\n" if i % 4 == 0
  fh.print "#{percentile_6[i]},"
end
fh.puts("]")

fh = File.open("percentiles_7.py", "w")
fh.puts("percentiles_7_cards = [")
(0..7461).each do |i|
  fh.print "\n" if i % 4 == 0
  fh.print "#{percentile_7[i]},"
end
fh.puts("]")