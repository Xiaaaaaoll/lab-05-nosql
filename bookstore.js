// Step 2: switch to the bookstore database
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
// One book by a new author (author_004), one by an existing author (author_002)
db.books.insertMany([
  {
    title: "Harry Potter and the Philosopher's Stone",
    published_year: 1997,
    author_ids: ["author_004"]
  },
  {
    title: "Coraline",
    published_year: 2002,
    author_ids: ["author_002"]
  }
])

// Step 7: add missing authors
// author_002 is already loaded; author_004 is new
db.authors.insertOne({
  _id: "author_004",
  name: "J.K. Rowling",
  nationality: "British",
  bio: {
    short: "British author best known for the Harry Potter series.",
    long: "J.K. Rowling is a British author whose Harry Potter series, beginning with Harry Potter and the Philosopher's Stone in 1997, became one of the best-selling book series in history."
  }
})

// Step 8: filter books by a list of authors (one loaded, one added)
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())
