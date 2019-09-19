#!/bin/bash

sudo kill $(cat pid/*.pid) && rm pid/*.pid
