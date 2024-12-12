
from collections import defaultdict
from huggingface_hub import HfApi
api = HfApi()




print("Top 10 most downloaded models by Helsinki-NLP:\n")

for m in api.list_models(sort="downloads", author="Helsinki-NLP",direction=-1, limit=10):
    print(f"{m.downloads}\t{m.id}\t{m.likes}")


print("\nTop 10 most liked models by Helsinki-NLP:\n")
for m in api.list_models(sort="likes", author="Helsinki-NLP",direction=-1, limit=10):
    print(f"{m.likes}\t{m.id}\t{m.downloads}")


downloads = 0
likes = 0
for m in api.list_models(author="Helsinki-NLP"):
    downloads += m.downloads
    likes += m.likes

print(f"\ntotal number of downloads for Helsinki-NLP models: {downloads}")
print(f"total number of likes for Helsinki-NLP models: {likes}")



print("\nTop 10 most downloaded datasets by Helsinki-NLP:\n")

for m in api.list_datasets(sort="downloads", author="Helsinki-NLP",direction=-1, limit=10):
    print(f"{m.downloads}\t{m.id}\t{m.likes}")


downloads = 0
likes = 0
for m in api.list_datasets(author="Helsinki-NLP"):
    downloads += m.downloads
    likes += m.likes

print(f"\ntotal number of downloads for Helsinki-NLP datasets: {downloads}")
print(f"total number of likes for Helsinki-NLP datasets: {likes}\n")




authorDownloads = defaultdict(int)
authorLikes = defaultdict(int)


# for m in api.list_models(limit=100, sort="downloads"):
for m in api.list_models(sort="downloads"):
    if m.downloads == 0:
        break
    id = m.id.split('/')
    authorDownloads[id[0]] += m.downloads
    authorLikes[id[0]] += m.likes



print("Top 50 organisations with the most downloads:\n")

count = 0
for d in sorted(authorDownloads, key=authorDownloads.get, reverse=True):
    count += 1
    print(f"{count}.\t{authorDownloads[d]}\t{authorLikes[d]}\t{d}")
    if count >= 50:
        break


print("\nComplete list of downloaded models by Helsinki-NLP:\n")

for m in api.list_models(sort="downloads", author="Helsinki-NLP",direction=-1):
    print(f"{m.downloads}\t{m.id}\t{m.likes}")

    
print("\nComplete list of downloaded datasets by Helsinki-NLP:\n")

for m in api.list_datasets(sort="downloads", author="Helsinki-NLP",direction=-1):
    print(f"{m.downloads}\t{m.id}\t{m.likes}")
