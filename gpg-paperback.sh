#!/bin/bash

KEY=6A9FB506

CHUNKSIZE=512
KEYFILE=$KEY.key.asc
QR_EC_LEVEL=H
TYPE=PNG

EXT=$(echo $TYPE | tr '[:upper:]' '[:lower:]')

rm $KEY.sums

#gpg --no-default-keyring --secret-keyring tmp/secring.gpg --list-secret-keys
gpg2 --no-default-keyring --secret-keyring tmp/secring.gpg --armor --export-secret-key $KEY > $KEYFILE

split --suffix-length=1 --bytes=$CHUNKSIZE $KEYFILE $KEYFILE

#for kf in $KEYFILE?; do echo $kf; done
for KF in $KEYFILE?
do
    sha256sum $KF >> $KEY.sums
    cat $KF | qrencode --level=$QR_EC_LEVEL --type=$TYPE --output=$KF.$EXT
done
#qrencode --level=H --type=EPS --output=$i.eps

test () {

    for QR in $KEYFILE?.$EXT
    do
	echo -n "$(zbarimg --raw $QR)" > $QR.xml
	sha256sum $QR.xml >> $KEY.sums
    done
}

test
