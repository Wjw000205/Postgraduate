import arxiv

# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "computer vision",
  max_results = 1,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

# `results` is a generator; you can iterate over its elements one by one...
i=0
for r in client.results(search):
  # print(r.title)
  print("第"+str(i+1)+"篇文章标题：" + str(r.title))
  i = i + 1
# ...or exhaust it into a list. Careful: this is slow for large results sets.
all_results = list(results)
i=0
for r in all_results:
    print("第"+str(i+1)+"篇文章的链接："+str(r))
    i = i+1
# print([r.title for r in all_results])

# # For advanced query syntax documentation, see the arXiv API User Manual:
# # https://arxiv.org/help/api/user-manual#query_details
# search = arxiv.Search(query = "au:del_maestro AND ti:checkerboard")
# first_result = next(client.results(search))
# print(first_result)
#
# # Search for the paper with ID "1605.08386v1"
# search_by_id = arxiv.Search(id_list=["1605.08386v1"])
# # Reuse client to fetch the paper, then print its title.
# first_result = next(client.results(search))
# print(first_result.title)
paper = next(arxiv.Client().results(arxiv.Search(id_list=["2504.20998v1"])))
# Download the archive to a specified directory with a custom filename.
paper.download_pdf(dirpath="./paper_dir", filename="downloaded-paper.pdf")