import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


class Media:
    def __init__(
        self, title: str, type: str, genre: str, year: int, rating: float, watched: bool
    ):
        self.title = title
        self.type = type
        self.genre = genre
        self.year = year
        self.rating = rating
        self.watched = watched

    def display_info(self) -> str:
        return f"""
            Title: {self.title.title()}
            Type: {self.type.capitalize()}
            Genre: {self.genre}
            Year: {self.year}
            Rating: {self.rating}
            Watched: {"Yes" if self.watched else "No"}
        """

    def __str__(self) -> str:
        return f"{self.title} ({self.type}) - {self.rating}"


class MediaRepository:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[Media]:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
                media_list = []
                for item in data:
                    media = Media(
                        title=item["title"],
                        type=item["type"],
                        genre=item["genre"],
                        year=item["year"],
                        rating=item["rating"],
                        watched=item["watched"],
                    )
                    media_list.append(media)
                return media_list
        except FileNotFoundError:
            print(f"Error: The file {self.path} was not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: The file {self.path} is not a valid JSON file.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def save(self, media_list: list[Media]) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                data = []
                for media in media_list:
                    item: dict[str, str | int | float | bool] = {
                        "title": media.title,
                        "type": media.type,
                        "genre": media.genre,
                        "year": media.year,
                        "rating": media.rating,
                        "watched": media.watched,
                    }
                    data.append(item)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            print(f"Error: The file {self.path} was not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error: The file {self.path} is not a valid JSON file.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []


class TXTReportManger:
    def __init__(self):
        self.file_path = "media_report.txt"

    def create_report(
        self,
        media_list: list[Media],
        total_media: int,
        watched: int,
        unwatched: int,
        Movies: int,
        Series: int,
        Average_rating: float,
    ) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(f"""
                    ===== MEDIA REPORT =====

                    Total media: {total_media}
                    Watched: {watched}
                    Unwatched: {unwatched}

                    Movies: {Movies}
                    Series: {Series}

                    Average rating: {Average_rating:.2f}
                    """)
        except PermissionError:
            print(f"[Denied access]: can't access {self.file_path}")
        except Exception as e:
            print(f"[Error]: something gone wrong, error = {e}")


class MediaClient:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def recommend_media(self, title: str, genre: str | None = None) -> Media | None:
        interaction = self.client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=(
                f"Recommend one movie or series similar to '{title}' "
                f"in the genre '{genre if genre is not None else 'any genre'}'. "
                "Return only a valid JSON object with these keys: "
                "title, type, genre, year, rating, watched. "
                "Use movie or series for type, an integer for year, "
                "a float from 0.0 to 10.0 for rating, and true or false for watched."
            ),
        )

        raw_text = interaction.output_text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        try:
            data = json.loads(raw_text)
            return Media(
                title=data["title"],
                type=data["type"],
                genre=data["genre"],
                year=int(data["year"]),
                rating=float(data["rating"]),
                watched=bool(data["watched"]),
            )
        except json.JSONDecodeError:
            print(f"[Error]: Model did not return valid JSON:\n{raw_text}")
            return None
        except (KeyError, ValueError) as e:
            print(f"[Error]: Missing or invalid field in model response: {e}")
            return None


class MediaEngine:
    def __init__(self, path: str = "media.json", api_key: str = API_KEY):
        self.repo = MediaRepository(path)
        self.repository: list[Media] = self.repo.load()
        self.dirty: bool = False
        self.report = TXTReportManger()
        self.client = MediaClient(api_key=api_key)

    def save(self) -> None:
        self.repo.save(media_list=self.repository)
        self.dirty = False

    def add_media(self, media: Media) -> None:
        self.repository.append(media)
        self.dirty = True

    def show_all_media(self) -> list[Media]:
        return self.repository

    def show_highest_rated_media(self) -> list[Media]:
        if not self.repository:
            return []
        highest_rating = max(media.rating for media in self.repository)
        return [media for media in self.repository if media.rating == highest_rating]

    def show_watched_media(self) -> list[Media]:
        return [media for media in self.repository if media.watched]

    def show_unwatched_media(self) -> list[Media]:
        return [media for media in self.repository if not media.watched]

    def search_media(self, title: str, genre: str | None = None) -> list[Media]:
        return [
            media
            for media in self.repository
            if title.lower() in media.title.lower()
            and (genre is None or genre.lower() in media.genre.lower())
        ]

    def remove_media(self, media: Media) -> None:
        self.repository.remove(media)
        self.dirty = True

    def update_rating(self, media: Media, new_rating: float):
        if media in self.repository:
            media.rating = new_rating
            self.dirty = True
        else:
            print(f"[Error]: Media '{media.title}' not found in the repository.")

    def mark_as_watched(self, media: Media):
        if media in self.repository:
            media.watched = True
            self.dirty = True
        else:
            print(f"[Error]: Media '{media.title}' not found in the repository.")

    def generate_report(self) -> None:
        media_list: list[Media] = self.repository
        total_media: int = len(media_list)
        watched: int = len([k for k in media_list if k.watched])
        unwatched: int = total_media - watched
        Movies: int = len([k for k in media_list if k.type == "movie"])
        Series: int = len([k for k in media_list if k.type == "series"])
        Ratings: list[float] = [k.rating for k in media_list]
        total_ratings: float = 0
        for Rating in Ratings:
            total_ratings += Rating
        Average_rating: float = (total_ratings) / total_media if total_media else 0.0
        self.report.create_report(
            media_list=media_list,
            total_media=total_media,
            watched=watched,
            unwatched=unwatched,
            Movies=Movies,
            Series=Series,
            Average_rating=Average_rating,
        )

    def recommend_media(self, title: str, genre: str | None = None) -> Media | None:
        return self.client.recommend_media(title=title, genre=genre)


class MediaCLI:
    def __init__(self, path: str = "media.json"):
        self.engine = MediaEngine(path=path)

    def run(self):
        print("====Welcome to the Media Manager!====")
        while True:
            choice: int = int(
                input("""
                1 - Show All Media
                2 - Add Media
                3 - Remove Media
                4 - Update Rating
                5 - Mark as Watched
                6 - Search Media
                7 - Show Highest Rated Media
                8 - Show Watched Media
                9 - Show Unwatched Media
                10 - Recommend Media
                11 - Exit
                CHOOSE a number 1 to 11
            """)
            )
            match choice:
                case 1:
                    media_list: list[Media] = self.engine.show_all_media()
                    print("====All Media====")
                    for i, media in enumerate(media_list):
                        print(f"{i + 1}. {media}")

                case 2:
                    try:
                        title: str = input("Enter the title: ")
                        type: str = input("Enter the type (movie/series): ")
                        genre: str = input("Enter the genre: ")
                        year: int = int(input("Enter the year: "))
                        rating: float = float(input("Enter the rating: "))
                        watched_input = (
                            input("Have you watched it? (yes/no): ").strip().lower()
                        )
                        watched: bool = True if watched_input == "yes" else False
                    except ValueError:
                        print("Invalid input. Please enter valid values.")
                        continue
                    media = Media(
                        title=title,
                        type=type,
                        genre=genre,
                        year=year,
                        rating=rating,
                        watched=watched,
                    )
                    self.engine.add_media(media=media)
                    print(f"Media: {media.title} is added successfully!")

                case 3:
                    title: str = input("Enter the title of the media to remove: ")
                    media_list: list[Media] = self.engine.search_media(title=title)
                    if not media_list:
                        print(f"No media found with title '{title}'.")
                    else:
                        print("====Search Results====")
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")
                        index: int = (
                            int(input("Enter the number of the media to remove: ")) - 1
                        )
                        if 0 <= index < len(media_list):
                            self.engine.remove_media(media_list[index])
                            print(
                                f"Media '{media_list[index].title}' removed successfully."
                            )
                        else:
                            print("Invalid selection.")

                case 4:
                    title: str = input(
                        "Enter the title of the media to update rating: "
                    )
                    media_list: list[Media] = self.engine.search_media(title=title)
                    if not media_list:
                        print(f"No media found with title '{title}'.")
                    else:
                        print("====Search Results====")
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")
                        index: int = (
                            int(
                                input(
                                    "Enter the number of the media to update rating: "
                                )
                            )
                            - 1
                        )
                        if 0 <= index < len(media_list):
                            new_rating = float(
                                input(
                                    f"Enter the new rating between 0 and 10, (old rating is = {media_list[index].rating})"
                                )
                            )
                            self.engine.update_rating(
                                media=media_list[index], new_rating=new_rating
                            )
                            print(
                                f"Media '{media_list[index].title}' rating updated successfully."
                            )
                        else:
                            print("Invalid selection.")

                case 5:
                    title: str = input(
                        "Enter the title of the media to mark as watched: "
                    )
                    media_list: list[Media] = self.engine.search_media(title=title)
                    if not media_list:
                        print(f"No media found with title '{title}'.")
                    else:
                        print("====Search Results====")
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")
                        index: int = (
                            int(
                                input(
                                    "Enter the number of the media to mark as watched: "
                                )
                            )
                            - 1
                        )
                        if 0 <= index < len(media_list):
                            self.engine.mark_as_watched(media=media_list[index])
                            print(
                                f"Media '{media_list[index].title}' marked as watched successfully."
                            )
                        else:
                            print("Invalid selection.")

                case 6:
                    title = input("Enter a title: ")
                    genre = input("Enter a genre (optional): ")
                    genre = genre.strip() or None
                    media_list: list[Media] = self.engine.search_media(
                        title=title, genre=genre
                    )
                    if not media_list:
                        print("No matching media found.")
                    else:
                        print("====Search Results====")
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")

                case 7:
                    media_list: list[Media] = self.engine.show_highest_rated_media()
                    print("====Highest Rated Media====")
                    if not media_list:
                        print("No media found.")
                    else:
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")

                case 8:
                    media_list: list[Media] = self.engine.show_watched_media()
                    print("====Watched Media====")
                    if not media_list:
                        print("No watched media found.")
                    else:
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")

                case 9:
                    media_list: list[Media] = self.engine.show_unwatched_media()
                    print("====UnWatched Media====")
                    if not media_list:
                        print("No unwatched media found.")
                    else:
                        for i, media in enumerate(media_list):
                            print(f"{i + 1}. {media}")

                case 10:
                    title = input("Enter a title: ")
                    genre = input("Enter a genre (optional): ")
                    genre = genre.strip() or None
                    media = self.engine.recommend_media(title=title, genre=genre)
                    if media:
                        print(
                            f"Recommended: {media.title} ({media.type}) - {media.rating}"
                        )
                        self.engine.add_media(media=media)
                    else:
                        print("No recommendations found.")

                case 11:
                    self.engine.generate_report()
                    print("Exiting...")
                    self.engine.save()
                    return

                case _:
                    print("invalid chioce!! \n choose again")


if __name__ == "__main__":
    program: MediaCLI = MediaCLI(path="media.json")
    program.run()
