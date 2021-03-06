
# Timelapse_EQ

Timelapse_EQ is a personal project I undertook after being intrigued by a [youtube video by Devon Crawford](https://www.youtube.com/watch?v=mHV6nb_4a-c). I used to spend a lot of time doing photography, and the idea of automating the process of adjusting photo exposures for a timelapse seemed very enticing.

![Timelapse Example](timelapse.gif)

## Installation

Grab a copy of the repo, and inside the project root, execute:

```
$ pip3 install .
```

From there you should be able to use timelapse_eq in bash.

## Usage

### Arguments

| Argument        | Description |
|-----------------|-------------|
| `directory`     | The only required argument. This is the path to the photos you want to work with. A "." would be your current directory. |
| `--start`       | If exposure change in the original photos began after the first photo, this flag will let you select where EV changes began from a list of filenames. |
| `--width WIDTH` | Where WIDTH is an integer, this will set the width of the output photo files. |
| `--auto-wb`     | This flag will apply auto-white-balance to the output files |

### Sample Usage

Let's take this for example:

```
$ timelapse_eq . --auto-wb --width 500 --start
```

What this is saying is:
 - We are in the directory that has the photos we want to work with.
 - We also want the output photos to have auto-white-balance applied.
 - The width of the output photos should be 500 pixels wide.
 - The start flag says give me the option to select a new start point for the EV changes.

Without the `--start` flag, the program will go on and not require any input from the user.

With the `--start` flag, something like this will pop up:

```
1: ./DSC_0771.NEF
2: ./DSC_0772.NEF
3: ./DSC_0773.NEF
4: ./DSC_0774.NEF
5: ./DSC_0775.NEF
6: ./DSC_0776.NEF
7: ./DSC_0777.NEF
8: ./DSC_0778.NEF
Enter number of new start point:
```

Then you would simply enter the number that corresponds with the file where the exposure started to change.
This will only display the files up to the first change in the EXIF data of the files provided.
Entering 1 would be the same as running the program without the `--start` flag.
