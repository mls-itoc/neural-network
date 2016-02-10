require 'open-uri'
require 'net/http'
require 'pry'
require 'json'

API_KEY = 'AIzaSyAsquULa5toOlgIAs6IRLW9WBPKWrlLBPo'
SEARCH_ENGIN_ID = '012674345528299337892:vr8sgv7eqcs'

def get_request(search_query: '美女', start_index: 1)
  url = "https://www.googleapis.com/customsearch/v1?key=#{API_KEY}&cx=#{SEARCH_ENGIN_ID}&searchType=image&q=#{search_query}&start=#{start_index}"
  encoded_url = URI.escape(url)
  uri = URI.parse(encoded_url)

  https = Net::HTTP.new(uri.host, uri.port)
  https.use_ssl = true

  https.start do
    https.get(uri.request_uri)
  end
end

def download_image(url)
  url = url.gsub(/(\?.+)/, "")
  file_name = File.basename(url)
  return nil unless file_name.downcase.match(/\.png|\.jpg|\.jpeg/)
  file_path = Dir.pwd + "/bijin_images/" + file_name
  open(file_path, 'wb') do |output|
    begin
      open(url) { |data| output.write(data.read) }
    rescue => e
      puts e.class
    end
  end
end

count = 0
start_index = 1

# とりあえず5000枚ダウンロードする
max_count = 5000
loop do
  puts "start count: #{count}"

  break if count == max_count || !start_index

  puts "start get_request"
  res = get_request(start_index: start_index)

  if res.code == '200'
    puts "status_code: 200"
    hash = JSON.parse(res.body)

    hash["items"].map do |item|
      download_image(item["link"])
    end

    next_page_node = hash.dig("queries", "nextPage")

    if next_page_node
      start_index = next_page_node.first["startIndex"]
    else
      puts "not found start index"
      start_index = nil
    end
  else
    puts "google return status_code: #{res.code}."
    next
  end
  count += 1
end



