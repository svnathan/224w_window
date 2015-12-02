#!/bin/bash

TotalTime="$(date +%s)"

source workDir.sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${red}Week $1${reset}"

item='Cell_Phones_and_Accessories'
goodRating='3'
year=(2008 2009 2010) # Mention years for parser_two_graphs.py file
recommendYear=2010
week=$1

directory=$directory$item"_"$week"/"
rm -rf $directory
mkdir -p $directory

T="$(date +%s)"
python parser_two_graphs.py $directory $directoryReviews $directoryItems $item $goodRating $week ${year[*]}
T="$(($(date +%s)-T))"

echo "${green}Completed Parsing in ${T} seconds${reset}"

T="$(date +%s)"
python centrality.py $directory $item
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Centrality for Items and Users in ${T} seconds${reset}"

infomapItemsInput=$directory"Edge_List_Items_"$item".txt"
infomapItemsOutput=$directory
cnmItemsFile=$directory"Community_Items_"$item".txt"

T="$(date +%s)"
#python communitycnm.py $infomapItemsInput $cnmItemsFile
Infomap $infomapItemsInput $infomapItemsOutput -z -2 -u
T="$(($(date +%s)-T))"

echo "${green}Completed Infomap for Items in ${T} seconds${reset}"

infomapUsersInput=$directory"Edge_List_Users_"$item".txt"
infomapUsersOutput=$directory
cnmUsersFile=$directory"Community_Users_"$item".txt"

T="$(date +%s)"
#python communitycnm.py $infomapUsersInput $cnmUsersFile
Infomap $infomapUsersInput $infomapUsersOutput -z -2 -u
T="$(($(date +%s)-T))"

echo "${green}Completed Infomap for Users in ${T} seconds${reset}"

treeItems=$directory"Edge_List_Items_"$item".tree"
edgeListItems=$directory"Edge_List_Items_"$item".txt"
clustersItemsOutputDirectory=$directory"Unanalyzed_Items_Clusters/"

mkdir -p $clustersItemsOutputDirectory

T="$(date +%s)"
#python create_input_PR_files.py $cnmItemsFile $edgeListItems $clustersItemsOutputDirectory
python create_input_PR_files.py $treeItems $edgeListItems $clustersItemsOutputDirectory
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Clusters for Items in ${T} seconds${reset}"

treeUsers=$directory"Edge_List_Users_"$item".tree"
edgeListUsers=$directory"Edge_List_Users_"$item".txt"
clustersUsersOutputDirectory=$directory"Unanalyzed_Users_Clusters/"

mkdir -p $clustersUsersOutputDirectory

T="$(date +%s)"
#python create_input_PR_files.py $cnmUsersFile $edgeListItems $clustersItemsOutputDirectory
python create_input_PR_files.py $treeUsers $edgeListUsers $clustersUsersOutputDirectory
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Clusters for Users in ${T} seconds${reset}"

nodesAtHopItemsOutput=$directory"Nodes_at_Hop_Items_Clusters/"

mkdir -p $nodesAtHopItemsOutput

T="$(date +%s)"
python nodes_at_hop.py $clustersItemsOutputDirectory $nodesAtHopItemsOutput
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Nodes at Hop for Items in ${T} seconds${reset}"

nodesAtHopUsersOutput=$directory"Nodes_at_Hop_Users_Clusters/"

mkdir -p $nodesAtHopUsersOutput

T="$(date +%s)"
python nodes_at_hop.py $clustersUsersOutputDirectory $nodesAtHopUsersOutput
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Nodes at Hop for Users in ${T} seconds${reset}"

T="$(date +%s)"
python recommend.py $directory $item $nodesAtHopUsersOutput $nodesAtHopItemsOutput
T="$(($(date +%s)-T))"

echo "${green}Completed Finding Recommendations in ${T} seconds${reset}"

T="$(date +%s)"
python recommendAnalyze.py $directory $directoryReviews $item $week $recommendYear
T="$(($(date +%s)-T))"

echo "${green}Completed Analyzing Recommendations in ${T} seconds${reset}"

TotalTime="$(($(date +%s)-TotalTime))"

echo "${red}Total Completion Time is ${TotalTime} seconds${reset}"