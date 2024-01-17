<h2 align=center><img src=https://media.giphy.com/media/IMDUAPmghzu2bxNY2K/giphy.gif width=50>Backend Api Downloader Tools <img src=https://media.giphy.com/media/LMt9638dO8dftAjtco/giphy.gif width=50></h2>


## Routes Api Endpoints

| Endpoints | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `/youtube` | `route` | Download from YouTube |
| `/instagram` | `route` | Download from Instagram  |
| `/tiktok` | `route` | Download from TikTok |
| `/twitter` | `route` | Download from Twitter / X |
| `/spotify` | `route` | Download from Spotify |



## Form data & Header For Auth

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |
| `source_link` | `string` | **Required**. The Source to be Downloaded  |
| `download_option` | `string` | **Except instagram and spotify**. Type of File to Download |

#### Source Link

```
  Example :
  youtube.com/link
  tiktok.com/link
  open.spotify.com/
  instagram.com/
  twitter.com/
```

#### Download Option

```
  Example :
  'image' for image
  'video' for video
  'audio' for audio
```


